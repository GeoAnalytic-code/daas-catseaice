#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  Icechart STAC Service
# Purpose:  Utility code for scraping websites and downloading files
# Author:   David Currie <dcurrie at geoanalytic dot com>
#
###############################################################################
# Copyright (c) 2020, David Currie <dcurrie at geoanalytic dot com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

from shapely.geometry import shape, MultiPolygon, mapping
from shapely.ops import transform
import fiona
import pyproj
import json


def extract_form_fields(soup):
    """Turn a BeautifulSoup form in to a dict of fields and default values"""
    fields = {}
    for input_fld in soup.findAll('input'):
        # ignore submit/image with no name attribute
        if input_fld['type'] in ('submit', 'image') or not input_fld.has_attr('name'):
            continue

        # single element name/value fields
        if input_fld['type'] in ('text', 'hidden', 'password', 'submit', 'image'):
            value = ''
            if input_fld.has_attr('value'):
                value = input_fld['value']
            fields[input_fld['name']] = value
            continue

        # checkboxes and radios
        if input_fld['type'] in ('checkbox', 'radio'):
            value = ''
            if input_fld.has_attr('checked'):
                if input_fld.has_attr('value'):
                    value = input_fld['value']
                else:
                    value = 'on'
            if input_fld['name'] in fields and value:
                fields[input_fld['name']] = value

            if input_fld['name'] not in fields:
                fields[input_fld['name']] = value

            continue

        assert False, 'input type %s not supported' % input_fld['type']

    # textareas
    for textarea in soup.findAll('textarea'):
        fields[textarea['name']] = textarea.string or ''

    # select fields
    for select in soup.findAll('select'):
        value = ''
        options = select.findAll('option')
        is_multiple = 'multiple' in select
        selected_options = [
            option for option in options
            if 'selected' in option
        ]

        # If no select options, go with the first one
        if not selected_options and options:
            selected_options = [options[0]]

        if not is_multiple:
            assert (len(selected_options) < 2)
            if len(selected_options) == 1:
                value = selected_options[0]['value']
        else:
            value = [option['value'] for option in selected_options]

        fields[select['name']] = value

    return fields


def extract_bbox_shape(shapefile: str):
    """ given a path to a shapefile, get the bounding box and outline geometry
    returns a dict containing the CRS of the original dataset, the bounding box and geometry as GeoJSON in both
    projected and latlong coordinates """
    wgs84 = pyproj.CRS('EPSG:4326')
    fin = fiona.open(shapefile)
    orig_crs = fin.crs
    orig_proj = pyproj.CRS(orig_crs)
    project = pyproj.Transformer.from_crs(orig_proj, wgs84, always_xy=True).transform
    mpt = MultiPolygon([shape(poly['geometry']) for poly in fin])
    fin.close()
    outline = mpt.convex_hull
    outline_wgs84 = transform(project, outline)
    bbox = mpt.minimum_rotated_rectangle
    bbox_wgs84 = transform(project, bbox)
    return {'crs': orig_crs,
            'pbbox': json.dumps(mapping(bbox)),
            'bbox': json.dumps(mapping(bbox_wgs84)),
            'pgeometry': json.dumps(mapping(outline)),
            'geometry': json.dumps(mapping(outline_wgs84))}
