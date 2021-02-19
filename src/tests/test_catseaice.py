#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  Icechart STAC Service
# Purpose:  Test StackDB class
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

import pytest
import pystac
from stackdb import StackDB
from icechart import IceChart
from catseaice import make_catalog


@pytest.fixture(scope='function')
def createdb():
    db = StackDB()
    yield db
    db.close()
    # assert type(db) is StackDB


@pytest.fixture(scope='function')
def additems(createdb):
    db = createdb
    # records can be added two ways, first as an IceChart item
    x = IceChart.from_name('rgc_a13_19730102_CEXPRGL',
                           'https://ice-glaces.ec.gc.ca/www_archive/AOI_13/Coverages/rgc_a13_19730102_CEXPRGL.e00')
    db.add_item(x)
    # or directly by name
    # x = IceChart.from_name('rgc_a10_20071015_CEXPRWA',
    #                        'https://ice-glaces.ec.gc.ca/www_archive/AOI_10/Coverages/rgc_a10_20071015_CEXPRWA.e00')
    # db.add_item(x)
    db.add_item_from_name('rgc_a10_20071015_CEXPRWA',
                          'https://ice-glaces.ec.gc.ca/www_archive/AOI_10/Coverages/rgc_a10_20071015_CEXPRWA.e00')

    x = IceChart.from_name('rgc_a11_20200120_CEXPREA',
                           'https://ice-glaces.ec.gc.ca/www_archive/AOI_11/Coverages/rgc_a11_20200120_CEXPREA.zip')
    db.add_item(x)
    x = IceChart.from_name('rgc_a11_20201207_CEXPREA',
                           'https://ice-glaces.ec.gc.ca/www_archive/AOI_11/Coverages/rgc_a11_20201207_CEXPREA.zip')
    db.add_item(x)
    x = IceChart.from_name('nic_arctic_20030106_pl_a',
                           'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Farctic%2F2003%2Fshapefiles%2Fhemispheric&fName=nic_arctic_20030106_pl_a.zip')
    db.add_item(x)
    x = IceChart.from_name('arctic060803',
                           'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Farctic%2F2006%2Fshapefiles%2Fhemispheric&fName=arctic060803.zip')
    db.add_item(x)
    x = IceChart.from_name('antarc170413',
                           'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Fantarctic%2F2017%2Fshapefiles%2Fhemispheric&fName=antarc170413.zip')
    db.add_item(x)
    x = IceChart.from_name('nic_antarc_20050207_pl_a',
                           'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Fantarctic%2F2005%2Fshapefiles%2Fhemispheric&fName=nic_antarc_20050207_pl_a.zip')
    db.add_item(x)

    # add the same record twice to ensure records are not duplicated
    x = IceChart.from_name('arctic060803',
                           'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Farctic%2F2006%2Fshapefiles%2Fhemispheric&fName=arctic060803.zip')
    db.add_item(x)
    x = IceChart.from_name('rgc_a11_20200120_CEXPREA',
                           'https://ice-glaces.ec.gc.ca/www_archive/AOI_11/Coverages/rgc_a11_20200120_CEXPREA.zip')
    db.add_item(x)
    yield db


def test_make_catalog(additems):
    db = additems
    # print(type(db))
    # print(isinstance(db, StackDB))
    catalog = make_catalog(db, source='NIC', region='antarctic', year='2005')
    assert type(catalog) == pystac.catalog.Catalog
    catalog.normalize_hrefs('/test')
    assert catalog.validate_all() is None
    assert catalog.description == 'Weekly Ice Charts From NIC for the year 2005 over the antarctic region'


def test_nomake_catalog(additems):
    """ check that make_catalog fails if no charts match the filter """
    db = additems
    # print(type(db))
    # print(isinstance(db, StackDB))
    catalog = make_catalog(db, source='CIS', region='Eastern Arctic', year='1999')
    assert catalog is None
