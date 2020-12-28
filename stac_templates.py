#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  Icechart STAC Service
# Purpose:  Template STAC Payloads for Ice Charts
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
NIC_ARCTIC_STAC = {"stac_version": "1.0.0-beta.2",
                   "stac_extensions": ["projection"],
                   "type": "Feature",
                   "id": "",
                   "bbox": [130.0867694444, 27.7226, -46.77297777778, 33.91436111111],
                   "geometry": {"type": "Polygon",
                                "coordinates": [[[130.0867694444, 27.7226],
                                                 [-135.0500472222, 32.42645833333],
                                                 [-46.77297777778, 33.91436111111],
                                                 [51.69973333333, 29.01120277778],
                                                 [130.0867694444, 27.7226]]]},
                   "properties": {"datetime": "2020-10-26",
                                  "collection": "NIC_Ice_Charts",
                                  "proj:epsg": None,
                                  "proj:wkt2": 'PROJCS["WGS_1984_Stereographic_North_Pole",GEOGCS["WGS 84",DATUM['
                                               '"WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG",'
                                               '"7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],'
                                               'UNIT["Degree",0.0174532925199433],AUTHORITY["EPSG","4326"]],'
                                               'PROJECTION["Polar_Stereographic"],PARAMETER["latitude_of_origin",60],'
                                               'PARAMETER["central_meridian",180],PARAMETER["false_easting",0],'
                                               'PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG",'
                                               '"9001"]],AXIS["Easting",SOUTH],AXIS["Northing",SOUTH]]',
                                  "region": "arctic"},
                   "links": [{"rel": "self",
                              "href": ""},
                             {"rel": "collection",
                              "href": ""}],
                   "assets": {"analytic": {
                       "href": "",
                       "type": "x-gis/x-shapefile",
                       "contents": [{"name": "2020_43_300.cnt"}]}
                   }
                   }

NIC_ANTARCTIC_STAC = {"stac_version": "1.0.0-beta.2",
                      "stac_extensions": ["projection"],
                      "type": "Feature",
                      "id": "",
                      "bbox": [128.300266666667, -29.0142305555556, -44.949952777778, -32.429377777778],
                      "geometry": {"type": "Polygon",
                                   "coordinates": [[[128.300266666667, -29.0142305555556],
                                                    [-135.0500472222, 32.42645833333],
                                                    [-44.949952777778, -32.429377777778],
                                                    [51.69973333333, 29.01120277778],
                                                    [128.300266666667, -29.0142305555556]]]},
                      "properties": {"datetime": "2020-10-26",
                                     "collection": "NIC_Ice_Charts",
                                     "proj:epsg": None,
                                     "proj:wkt2": 'PROJCS["WGS_1984_Stereographic_South_Pole",'
                                                  'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",'
                                                  'SPHEROID["WGS_1984",6378137.0,298.257223563]],'
                                                  'PRIMEM["Greenwich",0.0],UNIT["Degree",0.017453292519943295]],'
                                                  'PROJECTION["Stereographic_South_Pole"],'
                                                  'PARAMETER["False_Easting",0.0],'
                                                  'PARAMETER["False_Northing",0.0],'
                                                  'PARAMETER["Central_Meridian",180.0],'
                                                  'PARAMETER["standard_parallel_1",-60.0],'
                                                  'UNIT["Meter",1.0]]',
                                     "region": "antarctic"},
                      "links": [{"rel": "self",
                                 "href": ""},
                                {"rel": "collection",
                                 "href": ""}],
                      "assets": {"analytic": {
                          "href": "",
                          "type": "x-gis/x-shapefile",
                          "contents": [{"name": "2020_43_300.cnt"}]}
                      }
                      }

CIS_ARCTIC_STAC = {"stac_version": "1.0.0-beta.2",
                   "stac_extensions": ["projection"],
                   "type": "Feature",
                   "id": "",
                   "bbox": [130.0867694444, 27.7226, -46.77297777778, 33.91436111111],
                   "geometry": {"type": "Polygon",
                                "coordinates": [[[130.0867694444, 27.7226],
                                                 [-135.0500472222, 32.42645833333],
                                                 [-46.77297777778, 33.91436111111],
                                                 [51.69973333333, 29.01120277778],
                                                 [130.0867694444, 27.7226]]]},
                   "properties": {"datetime": "2020-10-26",
                                  "collection": "CIS_Ice_Charts",
                                  "proj:epsg": None,
                                  "proj:wkt2": 'PROJCS["WGS_1984_Stereographic_North_Pole",GEOGCS["WGS 84",DATUM['
                                               '"WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG",'
                                               '"7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],'
                                               'UNIT["Degree",0.0174532925199433],AUTHORITY["EPSG","4326"]],'
                                               'PROJECTION["Polar_Stereographic"],PARAMETER["latitude_of_origin",60],'
                                               'PARAMETER["central_meridian",180],PARAMETER["false_easting",0],'
                                               'PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG",'
                                               '"9001"]],AXIS["Easting",SOUTH],AXIS["Northing",SOUTH]]',
                                  "region": "arctic"},
                   "links": [{"rel": "self",
                              "href": ""},
                             {"rel": "collection",
                              "href": ""}],
                   "assets": {"analytic": {
                       "href": "",
                       "type": "x-gis/x-shapefile",
                       "contents": [{"name": "2020_43_300.cnt"}]}
                   }
                   }
