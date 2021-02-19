#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  Icechart STAC Service
# Purpose:  Test IceChart class
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

import datetime
from icechart import IceChart


def test_cistypes():
    x = IceChart.from_name('rgc_a09_20201214_CEXPRHB',
                 'https://ice-glaces.ec.gc.ca/www_archive/AOI_09/Coverages/rgc_a09_20201214_CEXPRHB.zip')
    assert x.epoch == datetime.datetime(2020, 12, 14, 0, 0)
    assert x.name == 'rgc_a09_20201214_CEXPRHB'
    assert x.format == 'ESRI SHAPEFILE'
    assert x.region == 'Hudson Bay'
    assert x.source == 'CIS'
    assert x.stac.validate() is None
    assert x.exactgeo == 0
    x = IceChart.from_name('rgc_a11_20161121_CEXPRHB',
                 'https://ice-glaces.ec.gc.ca/www_archive/AOI_11/Coverages/rgc_a11_20161121_CEXPRHB.e00')
    assert x.epoch == datetime.datetime(2016, 11, 21, 0, 0)
    assert x.format == 'ESRI E00'
    assert x.region == 'Eastern Arctic'
    assert x.source == 'CIS'
    assert x.stac.validate() is None


def test_nicarctictypes():
    x = IceChart.from_name('nic_arctic_20030106_pl_a',
                 'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Farctic%2F2003%2Fshapefiles%2Fhemispheric&fName=nic_arctic_20030106_pl_a.zip')
    assert x.epoch == datetime.datetime(2003, 1, 6, 0, 0)
    assert x.name == 'nic_arctic_20030106_pl_a'
    assert x.format == 'ESRI SHAPEFILE'
    assert x.region == 'arctic'
    assert x.source == 'NIC'
    assert x.stac.validate() is None
    x = IceChart.from_name('arctic060803',
                 'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Farctic%2F2006%2Fshapefiles%2Fhemispheric&fName=arctic060803.zip')
    assert x.epoch == datetime.datetime(2006, 8, 3, 0, 0)
    assert x.format == 'ESRI SHAPEFILE'
    assert x.region == 'arctic'
    assert x.source == 'NIC'
    assert x.stac.validate() is None


def test_nicantarctictypes():
    x = IceChart.from_name('antarc170413',
                 'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Fantarctic%2F2017%2Fshapefiles%2Fhemispheric&fName=antarc170413.zip')
    assert x.epoch == datetime.datetime(2017, 4, 13, 0, 0)
    assert x.format == 'ESRI SHAPEFILE'
    assert x.region == 'antarctic'
    assert x.source == 'NIC'
    assert x.stac.validate() is None
    x = IceChart.from_name('nic_antarc_20050207_pl_a',
                 'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Fantarctic%2F2005%2Fshapefiles%2Fhemispheric&fName=nic_antarc_20050207_pl_a.zip')
    assert x.epoch == datetime.datetime(2005, 2, 7, 0, 0)
    assert x.format == 'ESRI SHAPEFILE'
    assert x.region == 'antarctic'
    assert x.source == 'NIC'
    assert x.stac.validate() is None

def test_init():
    y = IceChart.from_name('antarc170413',
                 'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Fantarctic%2F2017%2Fshapefiles%2Fhemispheric&fName=antarc170413.zip')
    x = IceChart(y.__dict__)
    assert x.epoch == datetime.datetime(2017, 4, 13, 0, 0)
    assert x.format == 'ESRI SHAPEFILE'
    assert x.region == 'antarctic'
    assert x.source == 'NIC'
    assert x.stac.validate() is None

def test_exactgeo():
    x = IceChart.from_name('rgc_a09_20201214_CEXPRHB',
                 'https://ice-glaces.ec.gc.ca/www_archive/AOI_09/Coverages/rgc_a09_20201214_CEXPRHB.zip')
    assert x.exactgeo == 0
    x.exact_geometry()
    assert x.exactgeo == 1
    # try a shapefile that lacks projection metadata
    x = IceChart.from_name('nic_antarc_20050207_pl_a',
                 'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Fantarctic%2F2005%2Fshapefiles%2Fhemispheric&fName=nic_antarc_20050207_pl_a.zip')
    assert x.exactgeo == 0
    # this should fail
    x.exact_geometry()
    assert x.exactgeo == 0
    # try a good antarctic file
    x = IceChart.from_name('antarc170413',
                 'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Fantarctic%2F2017%2Fshapefiles%2Fhemispheric&fName=antarc170413.zip')
    assert x.exactgeo == 0
    # this should pass
    x.exact_geometry()
    assert x.exactgeo == 1
    # try a good arctic file
    x = IceChart.from_name('arctic060803',
                 'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Farctic%2F2006%2Fshapefiles%2Fhemispheric&fName=arctic060803.zip')
    assert x.exactgeo == 0
    # this should pass
    x.exact_geometry()
    assert x.exactgeo == 1
