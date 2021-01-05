#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  Icechart STAC Service
# Purpose:  Class for handling database of icecharts
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
import sqlite3
import json
from icechart import IceChart


class StackDB:
    """ a database (sqlite3) for storing IceChart objects """

    def __init__(self, name=':memory:'):

        self.conn = None
        self.cursor = None

        if name:
            self.open(name)

        self.create_tables()

    def open(self, name):

        try:
            self.conn = sqlite3.connect(name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            print("Error connecting to database!")

    def close(self):

        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        self.close()

    def get(self, table, columns, limit=None):

        query = "SELECT {0} from {1};".format(columns, table)
        self.cursor.execute(query)

        # fetch data
        rows = self.cursor.fetchall()

        return rows[len(rows) - limit if limit else 0:]

    def getlast(self, source='NIC'):
        """ returns the datetime of the oldest record for the selected source """
        sql = 'SELECT max(epoch) FROM items WHERE source = ?;'
        res = self.query(sql, (source,), fetch=True)[0][0]
        if res is not None:
            return datetime.datetime.strptime(res, "%Y-%m-%d %H:%M:%S")
        else:
            return None

    def write(self, table, columns, data):
        query = "INSERT INTO {0} ({1}) VALUES ({2});".format(table, columns, data)
        print(query)
        self.cursor.execute(query)

    def query(self, sql, qvars=(), fetch=False):
        """ execute an arbitrary SQL query
        if fetch is True, return a list of results """
        self.cursor.execute(sql, qvars)
        if fetch:
            return self.cursor.fetchall()

    def summary(self):
        """ return a dict of summary statistics for the items table """
        ret = {}
        # total items
        sql = 'SELECT COUNT(*) FROM items;'
        ret['Total Items'] = self.query(sql, fetch=True)[0][0]

        # list of sources
        ret['Sources'] = []
        sql = 'SELECT source FROM items GROUP BY source;'
        for x in self.query(sql, fetch=True):
            ret['Sources'].append(x[0])

        # count by source
        sql = 'SELECT source, count(source), min(epoch), max(epoch) FROM items GROUP BY source;'
        sct = self.query(sql, fetch=True)
        for src in sct:
            ret[src[0] + ' Count'] = src[1]
            ret[src[0] + ' Date Range'] = [datetime.datetime.strptime(src[2], '%Y-%m-%d %H:%M:%S').year,
                                           datetime.datetime.strptime(src[3], '%Y-%m-%d %H:%M:%S').year]

        # count by region
        for src in sct:
            sql = 'SELECT region, count(region), min(epoch), max(epoch) FROM items WHERE source=? GROUP BY region;'
            rct = self.query(sql, (src[0],), fetch=True)
            ret[src[0] + ' Regions'] = []
            for rgn in rct:
                ret[src[0] + ' Regions'].append(rgn[0])
                ret[' '.join((src[0], rgn[0], 'Count'))] = rgn[1]
                ret[' '.join((src[0], rgn[0], 'Date Range'))] = [
                    datetime.datetime.strptime(rgn[2], '%Y-%m-%d %H:%M:%S').year,
                    datetime.datetime.strptime(rgn[3], '%Y-%m-%d %H:%M:%S').year]
        return ret

    def create_tables(self):
        """ create table specifically for storing IceChart objects """
        sql = 'CREATE TABLE IF NOT EXISTS items (' \
              'name TEXT NOT NULL,' \
              'href TEXT NOT NULL,' \
              'source TEXT NOT NULL,' \
              'region TEXT NOT NULL,' \
              'epoch timestamp NOT NULL,' \
              'format TEXT NOT NULL,' \
              'stac TEXT NOT NULL, ' \
              'exactgeo INTEGER NOT NULL,' \
              'UNIQUE(source, epoch, region));'
        self.query(sql)

    def add_item(self, item: IceChart):
        """ Add an IceChart object to the items table """
        sql = 'INSERT OR REPLACE INTO items (name, href, source, region, epoch, format, stac, exactgeo)' \
              ' VALUES(?,?,?,?,?,?,?,?);'
        dt = (item.name, item.href, item.source, item.region, item.epoch, item.format, json.dumps(item.stac.to_dict()),
              item.exactgeo,)
        return self.cursor.execute(sql, dt)

    # get a list of items
    def get_items(self, source='Any', region='Any', epoch1='Any', epoch2='Any', exactgeo='Any') -> [IceChart]:
        """ return an iterable list of IceChart objects """
        sql = 'SELECT name, href, source, region, epoch, format, stac, exactgeo FROM ITEMS'
        dt = []
        w_cls = False
        if source != 'Any':
            sql = sql + ' WHERE source=?'
            w_cls = True
            dt.append(source)
        if region != 'Any':
            if w_cls:
                sql = sql + ' AND region=?'
            else:
                sql = sql + ' WHERE region=?'
            w_cls = True
            dt.append(region)
        if epoch1 != 'Any':
            if w_cls:
                sql = sql + ' AND epoch'
            else:
                sql = sql + ' WHERE epoch'
            dt.append(epoch1)
            if epoch2 != 'Any':
                sql = sql + ' BETWEEN ? AND ?'
                dt.append(epoch2)
            else:
                sql = sql + '=?'
        if exactgeo == 'False':
            if w_cls:
                sql = sql + ' AND NOT exactgeo'
            else:
                sql = sql + ' WHERE NOT exactgeo'
            w_cls = True
        if exactgeo == 'True':
            if w_cls:
                sql = sql + ' AND exactgeo'
            else:
                sql = sql + ' WHERE exactgeo'
            w_cls = True
        sql = sql + ' ORDER BY source, region, epoch DESC;'
        return self.query(sql, dt, fetch=True)

    def get_stac_items(self, source='Any', region='Any', year='All', limit=None):
        """ return a list of STAC objects """
        sql = 'SELECT stac FROM items'
        dt = []
        w_cls = False
        if source != "Any":
            w_cls = True
            sql = sql + ' WHERE source=?'
            dt.append(source)
        if region != 'Any':
            if w_cls:
                sql = sql + ' AND region=?'
            else:
                sql = sql + ' WHERE region=?'
            w_cls = True
            dt.append(region)
        if year != 'All':
            if w_cls:
                sql = sql + ' AND epoch BETWEEN ? AND ?'
            else:
                sql = sql + ' WHERE epoch BETWEEN ? AND ?'
            dt.append('{0}-01-01'.format(year))
            dt.append('{0}-12-31'.format(year))

        sql = sql + ' ORDER BY source, region, epoch DESC'
        if limit:
            sql = sql + ' LIMIT ?'
            dt.append(limit)

        sql = sql + ';'
        return self.query(sql, dt, fetch=True)
        # print(sql)
        # self.cursor.execute(sql, dt)
        # return self.cursor.fetchall()

    # get a record and return the column data as a dict or a STAC item (json)

    # return a collection

    #
