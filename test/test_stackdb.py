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
from stackdb import StackDB
from icechart import IceChart


@pytest.fixture(scope='function')
def createdb():
    db = StackDB()
    yield db
    db.close()
    # assert type(db) is StackDB


@pytest.fixture(scope='function')
def additems(createdb):
    db = createdb
    x = IceChart('rgc_a09_20201214_CEXPRHB',
                 'https://ice-glaces.ec.gc.ca/www_archive/AOI_09/Coverages/rgc_a09_20201214_CEXPRHB.zip')
    db.add_item(x)
    x = IceChart('rgc_a11_20161121_CEXPRHB',
                 'https://ice-glaces.ec.gc.ca/www_archive/AOI_11/Coverages/rgc_a11_20161121_CEXPRHB.e00')
    db.add_item(x)
    x = IceChart('nic_arctic_20030106_pl_a',
                 'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Farctic%2F2003%2Fshapefiles%2Fhemispheric&fName=nic_arctic_20030106_pl_a.zip')
    db.add_item(x)
    x = IceChart('arctic060803',
                 'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Farctic%2F2006%2Fshapefiles%2Fhemispheric&fName=arctic060803.zip')
    db.add_item(x)
    x = IceChart('antarc170413',
                 'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Fantarctic%2F2017%2Fshapefiles%2Fhemispheric&fName=antarc170413.zip')
    db.add_item(x)
    x = IceChart('nic_antarc_20050207_pl_a',
                 'https://usicecenter.gov/File/DownloadProduct?products=%2Fweekly%2Fantarctic%2F2005%2Fshapefiles%2Fhemispheric&fName=nic_antarc_20050207_pl_a.zip')
    db.add_item(x)
    yield db


def test_getitems(additems):
    db = additems
    result = db.get_stac_items(year=2016)
    assert len(result) == 1
    result = db.get_stac_items(source='NIC')
    assert len(result) == 4
    result = db.get_stac_items(region='antarctic')
    assert len(result) == 2

def test_summary(additems):
    db = additems
    summary = db.summary()
    assert summary['CIS Count'] == 2
    assert summary['NIC End Year'] == 2017

