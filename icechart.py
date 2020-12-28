#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  Icechart STAC Service
# Purpose:  Class for IceChart data
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
from datetime import datetime
from dateutil.parser import parse
import pystac
import stac_templates

CIS_AOI = {'a09': 'Hudson Bay',
           'a10': 'Western Arctic',
           'a11': 'Eastern Arctic',
           'a12': 'Eastern Coast',
           'a13': 'Great Lakes'
           }


class IceChart:
    """ An ice chart, which is a GIS file published by an Ice Service describing locations and characteristics of the
    sea ice regime for a specific point in time """

    def __init__(self, name: str, href: str):
        self.name = name
        self.href = href
        self.source = None
        self.region = None
        self.epoch = None
        self.format = None
        self.unpack_name()  # fill in the source, region, epoch and format values
        self.stac = None
        self.tostac()

    def unpack_name(self):
        """
        Given an icechart name extract the region, data type, and epoch info from the file name
        Supports the following types of filenames
        - NIC arctic:  eg  arctic180830.zip
        - Prototype NIC arctic shapefiles:  nic_arctic_20040301_pl_a.zip
        - NIC antarctic:  antarc140108.zip
        - Prototype NIC antarctic shapefiles:  nic_antarctic_20040301_pl_a.zip, antarc070810_polygon.zip
        - CIS e00 files:  rgc_a09_20161121_CEXPRHB.e00, rgc_a11_19680625_XXXXXX.e00
        - CIS shapefiles:  rgc_a09_20201214_CEXPRHB.zip
        - combined CIS files with the format cisarctic20180712.zip
        """
        fname = os.path.basename(self.href).lower()
        if len(fname):
            fpart, ext = os.path.splitext(fname)
            # if the href includes query code, assume the file name is at the end
            if '=' in fpart:
                fx = fpart.split('=')
                fpart = fx[len(fx)-1]
            # figure out the file format from the extension
            if '.e00' == ext:
                self.format = 'ESRI E00'
            elif '.zip' == ext:
                self.format = 'ESRI SHAPEFILE'
            else:
                self.format = 'UNKNOWN'

            # figure out source from the beginning of the file name
            if 'rgc' == fpart[:3] or 'cis' == fpart[:3]:
                self.source = 'CIS'
                if '_' in fpart:
                    cpts = fpart.split('_')
                    self.epoch = datetime.strptime(cpts[2], "%Y%m%d")
                    self.region = CIS_AOI[cpts[1]]
                else:
                    self.region = 'arctic'
                    self.epoch = datetime.strptime(fpart[-8:], "%Y%m%d")
            else:
                # if not CIS then NIC -- this will need more logic to support other sources
                self.source = 'NIC'
                if 'antarc' in fpart:
                    self.region = 'antarctic'
                else:
                    self.region = 'arctic'

                if '_' in fpart:
                    # deal with some bogus file names here
                    cpts = fpart.split('_')
                    if len(cpts) == 5:
                        self.epoch = datetime.strptime(cpts[2], "%Y%m%d")
                    else:
                        self.epoch = parse(fpart, fuzzy_with_tokens=True, yearfirst=True)[0]
                else:
                    self.epoch = parse(fpart, fuzzy_with_tokens=True, yearfirst=True)[0]

    def tostac(self):
        """ create a STAC item structure with whatever info we have """
        if self.source == 'NIC':
            if self.region == 'arctic':
                bplate = stac_templates.NIC_ARCTIC_STAC
            else:
                bplate = stac_templates.NIC_ANTARCTIC_STAC
        else:
            bplate = stac_templates.CIS_ARCTIC_STAC

        self.stac = pystac.Item(id=self.name,
                                geometry=bplate['geometry'],
                                bbox=bplate['bbox'],
                                datetime=self.epoch,
                                properties=bplate['properties'],
                                stac_extensions=bplate['stac_extensions'])

        self.stac.properties['region'] = self.region
        if self.format == 'ESRI SHAPEFILE':
            self.stac.add_asset(key='data', asset=pystac.Asset(href=self.href, media_type='x-gis/x-shapefile'))
        else:
            self.stac.add_asset(key='data', asset=pystac.Asset(href=self.href, media_type='application/x-ogc-avce00'))
