#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  Icechart STAC Service
# Purpose:  Main function - command line interface for creating Ice Chart stac catalogs
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

from icechart import IceChart
from stackdb import StackDB
from scrapers import gogetcisdata, gogetnicdata


def fill_database(dbname='icecharts.sqlite'):
    """ create a database and fill it with all available ice charts """
    print("Creating database {0}".format(dbname))
    db = StackDB(dbname)
    nicfiles = gogetnicdata()
    print("Adding {0} NIC files".format(len(nicfiles)))
    for nic in nicfiles:
        chart = IceChart(nic[0], nic[1])
        db.add_item(chart)
    cisfiles = gogetcisdata()
    print("Adding {0} CIS files".format(len(cisfiles)))
    for cis in cisfiles:
        chart = IceChart(cis[0], cis[1])
        db.add_item(chart)

    db.close()
