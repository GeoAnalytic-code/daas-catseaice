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
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from osgeo import ogr

from shapely.geometry import shape, MultiPolygon, mapping
from shapely.ops import transform
import fiona
from fiona.crs import to_string
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


def parse_htmlform_files(baseurl, form, payload, suffix, verify=True):
    """ post to an HTML form and parse the results for file links - returns a list of file names with links """
    r = requests.post(urljoin(baseurl, form), data=payload, verify=verify)
    # parse the results and pull out all the links to requested files
    soup = BeautifulSoup(r.text, 'html.parser')
    # loop through the available zip files and create a list for processing
    target_files = []
    for link in soup.find_all('a', text=re.compile(suffix)):
        filename = link.text.lower()
        # skip unexpected file names
        # if '_' in filename:
        #     continue
        target = urljoin(baseurl, link.attrs['href'])
        target_files.append([filename, target])
    return target_files


def biggest_bbox(bbox1: list, bbox2: list) -> list:
    """ given two bounding boxes, return a bbox encompassing both.
    if either inputs is an empty list, returns the other one """
    if len(bbox1) < 4:
        return bbox2
    if len(bbox2) < 4:
        return bbox1
    return([bbox1[0] if bbox1[0] < bbox2[0] else bbox2[0],
            bbox1[1] if bbox1[1] < bbox2[1] else bbox2[1],
            bbox1[2] if bbox1[2] > bbox2[2] else bbox2[2],
            bbox1[3] if bbox1[3] > bbox2[3] else bbox2[3]])


def extract_bbox_shape(shapefile: str, vfs: str = None):
    """ given a path to a shapefile, get the bounding box and outline geometry
    returns a dict containing the CRS of the original dataset, the bounding box and geometry as GeoJSON in both
    projected and latlong coordinates """
    wgs84 = pyproj.CRS('EPSG:4326')
    fin = fiona.open(shapefile, vfs=vfs)
    orig_crs = fin.crs
    orig_proj = pyproj.CRS(orig_crs)
    project = pyproj.Transformer.from_crs(orig_proj, wgs84, always_xy=True).transform
    mpt = MultiPolygon([shape(poly['geometry']) for poly in fin])
    fin.close()
    outline = mpt.convex_hull
    outline_wgs84 = transform(project, outline)
    bbox = mpt.minimum_rotated_rectangle
    bbox_wgs84 = transform(project, bbox)
    return {'crs': to_string(orig_crs),
            'pbbox': json.dumps(mapping(bbox)),
            'bbox': json.dumps(mapping(bbox_wgs84)),
            'pgeometry': json.dumps(mapping(outline)),
            'geometry': json.dumps(mapping(outline_wgs84))}


def test_url(href):
    """ make a HEAD request and return True if the status is 200 """
    r = requests.head(href)
    if r.status_code == 200:
        return True
    return False


def download_file(href, target):
    """ download a file from href to target """
    r = requests.get(href, stream=True)
    if r.status_code == 200:
        with open(target, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def get_vector_stats(href, intype='zip'):
    """ use OGR to get extents and SRID for a spatial dataset
    This isn't working for the new NIC server - need to download the files first """
    ogr.UseExceptions()
    # if intype = 'zip':   # assume this is a zipped shapefile
    inDriver = ogr.GetDriverByName('ESRI Shapefile')
    if intype == 'e00':  # for e00 files, download the file first
        inDriver = ogr.GetDriverByName('AVCE00')

    # what driver to use if not specified?
    target = href
    if 'http' in target:
        target = '/vsicurl/' + target
    if '.zip' in target:
        target = '/vsizip/' + target

    # open the file for read only
    ds = inDriver.Open(target, 0)
    # collect stats for each layer count
    stats = []
    try:
        for layer in range(ds.GetLayerCount()):
            lstats = {"Layer": layer}
            # get the layer, its SRID and extents
            l1 = ds.GetLayerByIndex(layer)
            lstats["name"] = l1.GetName()
            lstats["description"] = l1.GetDescription()
            lstats["features"] = l1.GetFeatureCount()
            lstats["metadata"] = l1.GetMetadata_Dict()
            if intype == 'zip' or (intype == 'e00' and lstats["name"] == 'PAL'):
                # skip these next time consuming steps on e00 files that are not polygon layers
                lstats["extents"] = l1.GetExtent()  # this should give a (projected?) bounding box
                lstats["srid"] = l1.GetSpatialRef().ExportToWkt()  # this should give a osr.SpatialReference object
            stats.append(lstats)
    except:
        pass

    # if srid.IsProjected():
    #     # convert bounding box to lat long
    #     llproj = osr.SpatialReference()
    #     t_srid = osr.SpatialReference()
    #     t_srid.ImportFromEPSG(4326)
    #     transform = osr.CoordinateTransformation(srid, t_srid)
    #     ul_p = ogr.CreateGeometryFromWkt("POINT ({0} {1})".format(ext[0], ext[1]))
    #     ll_p = ogr.CreateGeometryFromWkt("POINT ({0} {1})".format(ext[2], ext[3]))
    #     ul_p.Transform(transform)
    #     ll_p.Transform(transform)
    #     ext = (ul_p[0], ul_p[1], ll_p[0], ll_p[1])
    return stats
