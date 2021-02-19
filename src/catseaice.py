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
"""Create STAC Catalogs of Ice Charts

Usage:
  catseaice fill [-A | -S YYYY-MM-DD] [-e | -E] [-d DBNAME]
  catseaice report [-d DBNAME]
  catseaice write BASE_HREF [-t CTYPE] [-d DBNAME]
  catseaice (-h | --help)
  catseaice --version


Options:
  -h --help     Show this screen.
  --version     Show version.
  -S YYYY-MM-DD Start date for searching for icecharts
  -A            Search for all available icecharts (otherwise just update the database)
  -e            Calculate exact geometry for all newly discovered charts  (not usually required)
  -E            Calculate exact geometry for each chart in the database (not usually required)
  -d DBNAME     name of the database to use [default: icecharts.sqlite]
  BASE_HREF     root folder/url of output STAC catalog, default is the current directory [default: ...]
  -t CTYPE      STAC catalog type [default: SELF_CONTAINED]
                other valid values include ABSOLUTE_PUBLISHED and RELATIVE_PUBLISHED

"""

import os
from docopt import docopt
import json
import logging
import datetime
import pytz
import pprint
import pystac
from icechart import IceChart
from stackdb import StackDB
from scrapers import gogetcisdata, gogetnicdata
from utility import biggest_bbox

DBNAME = 'icecharts.sqlite'
STARTDATE = '1968-06-25'


def fill_database(dbname=DBNAME, startdate=STARTDATE, update=True, exactgeo=False):
    """ create a database and fill it with all available ice charts from startdate to the present
     if update is True, only search for data later than the latest date in the database """
    print("Using database {0}".format(os.path.abspath(dbname)))
    if update:
        print("Update from most recent records ")
    sdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    db = StackDB(dbname)
    if update:
        lastdate = db.getlast('NIC')
        if lastdate is not None:
            nicfiles = gogetnicdata(startyear=lastdate.year, startmonth=lastdate.month, startday=lastdate.day + 1)
        else:
            nicfiles = gogetnicdata(startyear=sdate.year, startmonth=sdate.month, startday=sdate.day)
    else:
        nicfiles = gogetnicdata(startyear=sdate.year, startmonth=sdate.month, startday=sdate.day)
    print("Adding or Updating {0} NIC files".format(len(nicfiles)))
    for nic in nicfiles:
        chart = IceChart.from_name(nic[0], nic[1])
        logging.info(chart.epoch.isoformat())
        if exactgeo:
            chart.exact_geometry()
        db.add_item(chart)
    # commit the changes in case we get interrupted
    db.conn.commit()

    if update:
        lastdate = db.getlast('CIS')
        if lastdate is not None:
            cisfiles = gogetcisdata(startyear=lastdate.year, startmonth=lastdate.month, startday=lastdate.day + 1,
                                    storefunc=db.add_item_from_name)
        else:
            cisfiles = gogetcisdata(startyear=sdate.year, startmonth=sdate.month, startday=sdate.day,
                                    storefunc=db.add_item_from_name)
    else:
        cisfiles = gogetcisdata(startyear=sdate.year, startmonth=sdate.month, startday=sdate.day,
                                storefunc=db.add_item_from_name)
    logging.info("Adding or Updating {0} CIS files".format(len(cisfiles)))
    # for cis in cisfiles:
    #     chart = IceChart.from_name(cis[0], cis[1])
    #     print(chart.epoch.isoformat())
    #     if exactgeo:
    #         chart.exact_geometry()
    #     db.add_item(chart)

    db.close()


def update_geometry(dbname, source='Any', region='Any', epoch1='Any', epoch2='Any'):
    """ download and analyze the source files to get accurate geometry """
    db = StackDB(dbname)
    rows = db.get_items(source=source, region=region, epoch1=epoch1, epoch2=epoch2, exactgeo='False')
    # print("Getting exact geometry for {0} records".format(len(rows)))
    for row in rows:
        r = dict(row)
        logging.info(f"Updating geometry for {r['name']}")
        r['stac'] = pystac.Item.from_dict(json.loads(r['stac']))
        chart = IceChart(dict(r))
        chart.exact_geometry()
        db.add_item(chart)
    db.close()


def make_catalog(dbs, source='NIC', region='arctic', year='2019',
                 catalog_type='SELF_CONTAINED', stacid='', description=''):
    """ create a STAC Catalog of items from the database
    Intended for creating sub-catalogs specific to a source/region/year combo
    returns the Catalog object or None on failure """
    if type(dbs) is str:
        db = StackDB(dbs)
    elif isinstance(dbs, StackDB):
        db = dbs
    else:
        logging.error(f'Please specify a database or database name {type(dbs)}')
        return

    # request all the records matching the filter params
    cis = db.get_stac_items(source=source, region=region, year=year)

    # create the catalog
    if len(stacid) < 1:
        stacid = ''.join([source, region, year]).replace(' ', '')
    if len(description) < 1:
        description = f'Weekly Ice Charts From {source} for the year {year} over the {region} region'
    catalog = pystac.Catalog(id=stacid, description=description,
                             catalog_type=catalog_type, stac_extensions=["projection"])

    # now add all the items to the catalog
    count = 0
    for cs in cis:
        count += 1
        stac = pystac.stac_object_from_dict(json.loads(cs[0]))
        catalog.add_item(stac)

    if count == 0:
        logging.warning(f'Database contains no entries for {source} {region} {year}')
        return

    logging.info(catalog.describe())
    return catalog


def make_collection(dbs, source='NIC', region='arctic', daterange=None, root_href='', stacid='',
                    description='', collection_license='proprietary'):
    """ create a collection of STAC items from the database
    """
    if type(dbs) is str:
        db = StackDB(dbs)
    elif isinstance(dbs, StackDB):
        db = dbs
    else:
        logging.error(f'Please specify a database or database name {type(dbs)}')
        return

    # make sure we have a proper date range
    if daterange is None:
        daterange = [1968, 2021]

    # set up a dummy extent, this will be updated later
    e_dict = {'spatial': {'bbox': [[-112.67872965304991,
                                    62.64083386314862,
                                    -21.96924552899297,
                                    82.38096680323945]]},
              'temporal': {'interval': [['2016-11-21T00:00:00Z', '2016-11-21T00:00:00Z']]}}
    extent = pystac.Extent.from_dict(e_dict)

    # create an empty collection
    if len(stacid) < 1:
        stacid = ''.join([source, region]).replace(' ', '')
    if len(description) < 1:
        description = f'Weekly Ice Charts From {source} over the {region} region'

    collection = pystac.Collection(id=stacid,
                                   description=description,
                                   extent=extent,
                                   license=collection_license)

    # create a catalog for each year and add to the collection
    count = 0
    for yr in range(daterange[0], daterange[1] + 1):
        ctlg = make_catalog(dbs, source=source, region=region, year=str(yr))
        if ctlg:
            collection.add_child(ctlg)
            count += 1

    logging.info(f"Added {count} yearly catalogs to collection for {source}{region}")
    if count == 0:
        return

    # tidy up the extents and references
    collection.update_extent_from_items()
    collection.normalize_hrefs(root_href=root_href)
    return collection


def save_catalog(dbname=DBNAME, catalog_type='SELF_CONTAINED', root_href=''):
    """ make a STAC catalog for all the data in the database, with collections organized by source, region, and year """
    db = StackDB(dbname)
    summary = db.summary()

    if summary['Total Items'] < 1:
        logging.warning('No data to save')
        db.close()
        return

    # if we don't get a root reference, assume we will use the current directory
    if root_href == '':
        root_href = os.getcwd()

    # the master catalog
    catalog = pystac.Catalog('icecharts', 'Weekly Ice Charts from NIC and CIS',
                             catalog_type=catalog_type, stac_extensions=["projection"])
    for source in summary['Sources']:
        logging.info(source)
        for region in summary[source + ' Regions']:
            logging.info(region)
            rgnclct = make_collection(db, source=source, region=region,
                                      daterange=summary[f'{source} {region} Date Range'])

            if rgnclct:
                catalog.add_child(rgnclct)

    catalog.normalize_and_save(root_href, catalog_type=catalog_type)
    db.close()


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Catalog Ice Charts 1.0')
    logging.info(arguments)

    if arguments['report']:
        db = StackDB(arguments['-d'])
        pprint.pprint(db.summary())
        db.close()
        quit()

    if arguments['fill']:
        if arguments['-E']:
            update_geometry(dbname=arguments['-d'])
        if arguments['-S']:
            fill_database(dbname=arguments['-d'], startdate=(arguments['-S']), update=False,
                          exactgeo=(arguments['-e'] | arguments['-E']))
        else:
            fill_database(dbname=arguments['-d'], update=(not arguments['-A']),
                          exactgeo=(arguments['-e'] | arguments['-E']))

    if arguments['write']:
        if arguments['BASE_HREF'] is None:
            arguments['BASE_HREF'] = ''
        save_catalog(dbname=arguments['-d'], catalog_type=arguments['-t'], root_href=arguments['BASE_HREF'])
