#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  Icechart STAC Service
# Purpose:  Scrape NIC and CIS web sites for ice charts
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
import sys
import shutil
import ssl
import glob
import zipfile
import datetime
from dateutil.parser import parse
import requests
import re
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin
from string import Template
from osgeo import ogr, osr

startyear = 1962
startmonth = 1
startday = 1

VERIFY = True
nic_basesite = 'https://www.natice.noaa.gov/products/'
nic_form = 'weekly_products.html'
cis_format_break = '2020-01-14'
cis_site_form = 'https://iceweb1.cis.ec.gc.ca/Archive/page1.xhtml?lang=en'


def parse_htmlform_files(baseurl, form, payload, suffix, verify=VERIFY):
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


def download_file(href, target):
    """ download a file from href to target """
    r = requests.get(href, stream=True)
    if r.status_code == 200:
        with open(target, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def get_vector_stats(href, intype='zip'):
    """ use OGR to get extents and SRID for a spatial dataset """
    ogr.UseExceptions()
    # if intype = 'zip':   # assume this is a zipped shapefile
    inDriver = ogr.GetDriverByName('ESRI Shapefile')
    if intype == 'e00':  # for e00 files, download the file first
        inDriver = ogr.GetDriverByName('AVCE00')
        # download_file(href, './test/test.e00')  # TODO: should use tempfile
        # href = './test/test.e00'

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
                lstats["extents"] = l1.GetExtent()       # this should give a (projected?) bounding box
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


def gogetnicdata():
    """ new and improved web scraping for NIC shapefiles
    returns a list of available files from the old NIC icechart server """
    # query the website for Arctic datasets between the given start date and today
    td = datetime.date.today()
    ts = datetime.date(startyear, startmonth, startday)
    target_files = []
    # first search for Arctic E00 files
    payload = {'oldarea': 'Arctic', 'oldformat': 'E00', 'year0': str(ts.year), 'month0': ts.strftime("%b"),
               'day0': str(ts.day).zfill(2), 'year1': str(td.year), 'month1': td.strftime("%b"),
               'day1': str(td.day).zfill(2), 'area': 'Arctic', 'format': 'E00', 'subareas': 'Hemispheric'}

    target_files.extend(parse_htmlform_files(nic_basesite, nic_form, payload, 'e00'))
    # Now search for Arctic shapefiles
    payload['oldformat'] = 'Shapefiles'
    payload['format'] = 'Shapefiles'
    target_files.extend(parse_htmlform_files(nic_basesite, nic_form, payload, 'zip'))

    # now do the antarctic - shapes
    payload['oldarea'] = 'Antarctic'
    payload['area'] = 'Antarctic'
    target_files.extend(parse_htmlform_files(nic_basesite, nic_form, payload, 'zip'))
    # finally antarctic E00
    payload['oldformat'] = 'E00'
    payload['format'] = 'E00'
    target_files.extend(parse_htmlform_files(nic_basesite, nic_form, payload, 'e00'))
    return target_files

    # for t in target_files:
    #     print('Downloading %s from %s' % (t[0], t[1]))
    #     targetfile = os.path.join(cfg.zippath, t[0])
    #     targeturl = t[1]
    #     # do some special gymnastics to get data in spite of expired certs
    #     # TODO: make this an option in DataSources
    #     if cfg.nic_verify:  # if the NIC server has a valid cert
    #         try:
    #             nicfile = requests.get(targeturl)
    #             with open(targetfile, 'wb') as out_file:
    #                 out_file.write(nicfile.content)
    #         except:
    #             print("Error downloading {0}".format(targeturl))
    #     else:   # if the cert is expired, use download anyway using urllib
    #         ctx = ssl.create_default_context()
    #         ctx.check_hostname = False
    #         ctx.verify_mode = ssl.CERT_NONE
    #         # need to catch errors in the request here
    #         try:
    #             source = urllib.request.urlopen(targeturl, context=ctx)
    #             print(source.status)
    #             with open(targetfile, 'wb') as out_file:
    #                 shutil.copyfileobj(source, out_file)
    #
    #         except Exception as inst:
    #             print(inst)
    #             pass


def gogetcisdata():
    """ retrieve e00 data from the CIS site
    Old data (from ??? to 01-2020) comes as an E00 file named like this: rgc_a10_20200106_CEXPRWA.e00
    new data (since 01-2020 comes as a zip file named like this:  rgc_a10_20200330_CEXPRWA.zip
        containing a shape file named like this (note the DDMMYYYY):      30032020_CEXPRWA.shp"""
    startdate = datetime.date(startyear, startmonth, startday)
    breakdate = datetime.datetime.strptime(cis_format_break, '%Y-%m-%d').date()
    # while startdate < datetime.date.today():
    #     targetresult = os.path.join(cfg.cis_resultsdir, startdate.strftime('%Y_%W_%j.cnt'))
    #     result_exists = CntGrid.objects.filter(data_source__iexact='CIS').filter(region__iexact='arctic').filter(
    #         epoch=startdate).exists()
    #     chart_exists = Icechart.objects.filter(data_source__iexact='CIS').filter(region__iexact='arctic').filter(
    #         epoch=startdate).exists()
    #
    #     if result_exists or chart_exists:
    #         print('Skipping CIS date %s' % startdate.isoformat())
    #     else:
    #         print('Retrieving CIS data for %s' % startdate.isoformat())
    #         for aoi, laoi, caoi in zip(cfg.aoi_list, cfg.laoi_list, cfg.caoi_list):
    #             if startdate < breakdate:
    #                 targeturl = Template(cfg.cis_baseurl).substitute(AOI=aoi, LAOI=laoi, CAOI=caoi,
    #                                                                  DATE=startdate.strftime('%Y%m%d_'))
    #                 targetfile = os.path.join(cfg.coveragepath, os.path.basename(targeturl))
    #             else:
    #                 targeturl = Template(cfg.cis_shp_baseurl).substitute(AOI=aoi, LAOI=laoi, CAOI=caoi,
    #                                                                      DATE=startdate.strftime('%Y%m%d_'))
    #                 targetfile = os.path.join(cfg.cis_zippath, os.path.basename(targeturl))
    #
    #             print(targeturl)
    #             try:
    #                 gotfile, headers = urllib.request.urlretrieve(targeturl, targetfile)
    #
    #             except Exception as inst:
    #                 print(inst)
    #                 pass
    #
    #     startdate = startdate + datetime.timedelta(weeks=1)
    return 0
