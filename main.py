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
import os
import json
import datetime
import pytz
import pystac
from icechart import IceChart
from stackdb import StackDB
from scrapers import gogetcisdata, gogetnicdata
from utility import biggest_bbox


def fill_database(dbname='icecharts.sqlite', update=True):
    """ create a database and fill it with all available ice charts
     if update is True, only search for data later than the latest date in the database """
    print("Creating database {0}".format(dbname))
    db = StackDB(dbname)
    if update:
        lastdate = db.getLast('NIC')
        nicfiles = gogetnicdata(startyear=lastdate.year, startmonth=lastdate.month, startday=lastdate.day)
    else:
        nicfiles = gogetnicdata()
    print("Adding {0} NIC files".format(len(nicfiles)))
    for nic in nicfiles:
        chart = IceChart(nic[0], nic[1])
        db.add_item(chart)

    if update:
        lastdate = db.getLast('CIS')
        cisfiles = gogetcisdata(startyear=lastdate.year, startmonth=lastdate.month, startday=lastdate.day)
    else:
        cisfiles = gogetcisdata()
    print("Adding {0} CIS files".format(len(cisfiles)))
    for cis in cisfiles:
        chart = IceChart(cis[0], cis[1])
        db.add_item(chart)

    db.close()


def make_collection(dbs, source='NIC', region='arctic', year='All', root_href='', stacid='',
                    description='', collection_license='MIT'):
    """ create a collection of STAC items """
    if type(dbs) is str:
        db = StackDB(dbs)
    elif type(dbs) is StackDB:
        db = dbs
    else:
        print('Please specify a database or database name')
        return

    cis = db.get_stac_items(source=source, region=region, year=year)
    if len(cis) < 1:
        print('No data found for source {0}, region {1}, year {2}'.format(source, region, year))
        return
    stacs = []
    spatial_extent = []
    mindate = datetime.datetime.now()
    maxdate = datetime.datetime.min
    # make the timestamp bounds offset aware so we can do comparisons
    mindate = mindate.replace(tzinfo=pytz.UTC)
    maxdate = maxdate.replace(tzinfo=pytz.UTC)
    for cs in cis:
        stac = pystac.stac_object_from_dict(json.loads(cs[0]))
        stacs.append(stac)

        mindate = stac.datetime if stac.datetime < mindate else mindate
        maxdate = stac.datetime if stac.datetime > maxdate else maxdate
        spatial_extent = biggest_bbox(spatial_extent, stac.bbox)

    extent = pystac.Extent(spatial=pystac.pystac.SpatialExtent(bboxes=[spatial_extent]),
                           temporal=pystac.TemporalExtent([[mindate, maxdate]]))
    collection = pystac.Collection(id=stacid,
                                   description=description,
                                   extent=extent,
                                   license=collection_license)
    collection.add_items(stacs)
    collection.normalize_hrefs(root_href=root_href)
    return collection


def save_catalog(dbname='icecharts.sqlite', catalog_type='SELF_CONTAINED', root_href=''):
    """ make a STAC catalog for all the data in the database, with collections organized by source, region, and year """
    db = StackDB(dbname)
    summary = db.summary()

    if summary['Total Items'] < 1:
        print('No data to save')
        db.close()
        return

    # if we don't get a root reference, assume we will use the current directory
    if root_href == '':
        root_href = os.getcwd()

    # the master catalog
    catalog = pystac.Catalog('icecharts', 'Weekly Ice Charts from NIC and CIS', catalog_type=catalog_type)
    for source in summary['Sources']:
        print(source)
        sroot_href = '/'.join([root_href,source])
        srccat = pystac.Catalog(source + '-icecharts', 'Weekly icecharts from ' + source, catalog_type=catalog_type)
        for region in summary[source + ' Regions']:
            print(region)
            rsroot_href = '/'.join([sroot_href, region])
            rgncat = pystac.Catalog('-'.join([source, region, 'icecharts']).strip(), 'Weekly icecharts for ' + region,
                                    catalog_type=catalog_type)
            for yr in range(summary['{0} {1} Date Range'.format(source, region)][0],
                            summary['{0} {1} Date Range'.format(source, region)][1]):
                print(yr)
                yrsroot_href = '/'.join([rsroot_href, str(yr)])
                collid = ''.join([source, region, str(yr), 'icecharts']).strip()
                coll = make_collection(db, source, region, str(yr), yrsroot_href, collid, 'Icecharts from ' + source)
                if coll:
                    rgncat.add_child(coll, title=collid)
            srccat.add_child(rgncat)
        catalog.add_child(srccat)

    catalog.normalize_and_save(root_href, catalog_type=catalog_type)
    print("Done???")
