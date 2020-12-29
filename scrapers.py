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
import datetime
from string import Template
from utility import parse_htmlform_files, test_url

# first available data from CIS appears to be 1968-06-25
STARTYEAR = 1968
STARTMONTH = 6
STARTDAY = 25

# define some constants for accessing the NIC website
VERIFY = True
nic_basesite = 'https://www.natice.noaa.gov/products/'
nic_basesite_new = 'https://usicecenter.gov/Products/DisplaySearchResults'
nic_ra = 'https://usicecenter.gov/Products/ArchiveSearch?table=WeeklyArctic&product=Arctic%20Weekly%20Shapefile&linkChange=arc-two'
nic_antarctic_new = 'https://usicecenter.gov/Products/ArchiveSearch?table=WeeklyAntarctic&product=Antarctic%20Weekly%20Shapefile&linkChange=ant-two'
nic_form = 'weekly_products.html'

# define some constants for accessing the CIS website
cis_format_break = '2020-01-14'
cis_e00_baseurl = 'https://ice-glaces.ec.gc.ca/www_archive/$AOI/Coverages/rgc_$LAOI$DATE$CAOI.e00'
cis_shp_baseurl = 'https://ice-glaces.ec.gc.ca/www_archive/$AOI/Coverages/rgc_$LAOI$DATE$CAOI.zip'
aoi_list = ['AOI_09', 'AOI_10', 'AOI_11', 'AOI_12', 'AOI_13']
laoi_list = ['a09_', 'a10_', 'a11_', 'a12_', 'a13_']
caoi_list = ['CEXPRHB', 'CEXPRWA', 'CEXPREA', 'CEXPREC', 'CEXPRGL']
cis_aoi_labels = ['Hudson Bay', 'Western Arctic', 'Eastern Arctic', 'Eastern Coast', 'Great Lakes']


def gogetnicdata(site='New', startyear=STARTYEAR, startmonth=STARTMONTH, startday=STARTDAY):
    """ new and improved web scraping for NIC shapefiles
    returns a list of available files from the old NIC icechart server """
    # query the website for Arctic datasets between the given start date and today
    td = datetime.date.today()
    ts = datetime.date(startyear, startmonth, startday)
    target_files = []
    if site == 'New':  # use the new (Dec 2020) site
        # ssn = requests.session()
        # baseurl = 'https://usicecenter.gov/Products/ArchiveSearch'
        # qry = {'table': 'WeeklyArctic', 'product': 'Arctic%20Weekly%20Shapefile', 'linkChange': 'arc-two'}
        # frm = ssn.get(baseurl, params=qry)
        # fmr.url
        # first search the arctic (zip files only as far as I can tell)
        payload = {'searchText': 'WeeklyArctic', 'searchProduct': 'Arctic Weekly Shapefile',
                   'startDate': ts.strftime("%m/%d/%Y"), 'endDate': td.strftime("%m/%d/%Y")}
        target_files.extend(parse_htmlform_files(nic_basesite_new, '', payload, 'zip', VERIFY))
        # now search for antarctic files
        payload = {'searchText': 'WeeklyAntarctic', 'searchProduct': 'Antarctic Weekly Shapefile',
                   'startDate': ts.strftime("%m/%d/%Y"), 'endDate': td.strftime("%m/%d/%Y")}
        target_files.extend(parse_htmlform_files(nic_basesite_new, '', payload, 'zip', VERIFY))
    else:
        # first search for Arctic E00 files
        payload = {'oldarea': 'Arctic', 'oldformat': 'E00', 'year0': str(ts.year), 'month0': ts.strftime("%b"),
                   'day0': str(ts.day).zfill(2), 'year1': str(td.year), 'month1': td.strftime("%b"),
                   'day1': str(td.day).zfill(2), 'area': 'Arctic', 'format': 'E00', 'subareas': 'Hemispheric'}

        target_files.extend(parse_htmlform_files(nic_basesite, nic_form, payload, 'e00', VERIFY))
        # Now search for Arctic shapefiles
        payload['oldformat'] = 'Shapefiles'
        payload['format'] = 'Shapefiles'
        target_files.extend(parse_htmlform_files(nic_basesite, nic_form, payload, 'zip', VERIFY))

        # now do the antarctic - shapes
        payload['oldarea'] = 'Antarctic'
        payload['area'] = 'Antarctic'
        target_files.extend(parse_htmlform_files(nic_basesite, nic_form, payload, 'zip', VERIFY))
        # finally antarctic E00
        payload['oldformat'] = 'E00'
        payload['format'] = 'E00'
        target_files.extend(parse_htmlform_files(nic_basesite, nic_form, payload, 'e00', VERIFY))
    return target_files


def gogetcisdata(startyear=STARTYEAR, startmonth=STARTMONTH, startday=STARTDAY):
    """ retrieve a list of e00 and zip data from the CIS site
    Old data (from ??? to 01-2020) comes as an E00 file named like this: rgc_a10_20200106_CEXPRWA.e00
    new data (since 01-2020 comes as a zip file named like this:  rgc_a10_20200330_CEXPRWA.zip
        containing a shape file named like this (note the DDMMYYYY):      30032020_CEXPRWA.shp"""
    startdate = datetime.date(startyear, startmonth, startday)
    breakdate = datetime.datetime.strptime(cis_format_break, '%Y-%m-%d').date()
    target_files = []
    while startdate < datetime.date.today():
        for aoi, laoi, caoi in zip(aoi_list, laoi_list, caoi_list):
            if startdate < breakdate:
                targeturl = Template(cis_e00_baseurl).substitute(AOI=aoi, LAOI=laoi, CAOI=caoi,
                                                                 DATE=startdate.strftime('%Y%m%d_'))
            else:
                targeturl = Template(cis_shp_baseurl).substitute(AOI=aoi, LAOI=laoi, CAOI=caoi,
                                                                     DATE=startdate.strftime('%Y%m%d_'))

            # print(targeturl)
            if test_url(targeturl):
                target_files.append([os.path.splitext(os.path.basename(targeturl))[0], targeturl])

        startdate = startdate + datetime.timedelta(weeks=1)

    return target_files
