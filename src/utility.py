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
import os
import re
from urllib.parse import urljoin
import tempfile
import zipfile
from zipfile import BadZipFile
import requests
from bs4 import BeautifulSoup

from shapely.geometry import shape, Point, Polygon, MultiPoint, MultiPolygon, mapping
from shapely.ops import transform
import fiona
import pyproj


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
    return ([bbox1[0] if bbox1[0] < bbox2[0] else bbox2[0],
             bbox1[1] if bbox1[1] < bbox2[1] else bbox2[1],
             bbox1[2] if bbox1[2] > bbox2[2] else bbox2[2],
             bbox1[3] if bbox1[3] > bbox2[3] else bbox2[3]])


def extract_bbox_shape(shapefile: str, vfs: str = None):
    """ given a path to a shapefile, get the bounding box and outline geometry
    returns a dict containing the CRS of the original dataset, the bounding box and geometry as GeoJSON in both
    projected and latlong coordinates """
    # define the lat/lon coordinate system and the poles
    wgs84 = pyproj.CRS('EPSG:4326')
    northpole = Point([0, 90])
    southpole = Point([0, -90])
    # open the file, note the virtual file system options for fiona
    # https://fiona.readthedocs.io/en/latest/fiona.html?highlight=fiona.open#fiona.open
    fin = fiona.open(shapefile, vfs=vfs)
    orig_crs = fin.crs
    crs_wk2 = fin.crs_wkt
    # get a multipolygon feature from all the features in the shapefile
    mpt = MultiPolygon([shape(poly['geometry']) for poly in fin])
    fin.close()
    # set up the coordinate tranformations and convert the poles
    orig_proj = pyproj.CRS(orig_crs)
    to_wgs84 = pyproj.Transformer.from_crs(orig_proj, wgs84, always_xy=True).transform
    from_wgs84 = pyproj.Transformer.from_crs(wgs84, orig_proj, always_xy=True).transform
    northpole_p = transform(from_wgs84, northpole)
    southpole_p = transform(from_wgs84, southpole)
    # compute the outline geometry of the multipolygon (this is all done in the projected coordinate system)
    outline = mpt.convex_hull
    # Now transform to WGS84, we will treat the data differently if it covers one of the poles
    # first - convert the outline polygon to a multipoint object
    outline_pts = MultiPoint(list(outline.exterior.coords))
    # next transform to WGS84, this time using pyproj directly
    outlinepts_wgs84 = transform(to_wgs84, outline_pts)
    if outline.contains(northpole_p):
        # a North polar outline
        # add a few points at the pole
        tpts = list(outlinepts_wgs84.geoms)
        tpts.append(Point(-179.9999, 90))
        tpts.append(Point(0, 90))
        tpts.append(Point(179.9999, 90))
        otlp_wgs84 = MultiPoint(tpts)
        # now get the convex hull of the new collection of points
        outline_wgs84 = otlp_wgs84.convex_hull
    elif outline.contains(southpole_p):
        # a South polar outline
        # add a few points at the pole
        tpts = list(outlinepts_wgs84.geoms)
        tpts.append(Point(-179.9999, -90))
        tpts.append(Point(0, -90))
        tpts.append(Point(179.9999, -90))
        otlp_wgs84 = MultiPoint(tpts)
        # now get the convex hull of the new collection of points
        outline_wgs84 = otlp_wgs84.convex_hull
    else:
        # if the pole isn't enclosed, we should be able to just transform the outline to lat/long
        outline_wgs84 = transform(to_wgs84, outline)

    return {'crs': crs_wk2,
            'pbbox': list(outline.bounds),
            'bbox': list(outline_wgs84.bounds),
            'pgeometry': mapping(outline),
            'geometry': mapping(outline_wgs84)}


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
        return target
    else:
        return None


def get_zipshape_bbox(href):
    """ download a zipped shapefile to a temporary folder and get its bounding box and shape """
    with tempfile.TemporaryDirectory() as tmpdir:
        zipfilename = os.path.join(tmpdir, 'temp.zip')
        if download_file(href, zipfilename):
            zipfl = zipfile.ZipFile(zipfilename)
            try:
                if zipfl.testzip():
                    print(f"Corrupt zip file {href}")
                    zipfl.close()
                    return
            except BadZipFile:
                print(f"Corrupt zip file {href}")
                return
            filelist = zipfl.namelist()
            zipfl.close()
            shpfiles = [s for s in filelist if s.endswith('.shp')]
            if len(shpfiles) > 0:
                # only read the first shapefile if there are more than one??
                return extract_bbox_shape(shpfiles[0], vfs='zip:' + zipfilename)
            else:
                print('No shapefiles found in archive {0}'.format(href))
                return
        else:
            print('Failed to download file {0}'.format(href))
            return
