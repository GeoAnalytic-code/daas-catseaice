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

CIS_HUDSONBAY_STAC = {"type": "Feature",
                      "stac_version": "1.0.0-beta.2",
                      "id": "rgc_a09_20201221_CEXPRHB",
                      "properties": {
                          "datetime": "2020-12-21T00:00:00Z",
                          "collection": "CIS_Ice_Charts",
                          "proj:epsg": None,
                          "proj:wkt2": "PROJCS[\"WGS_1984_Lambert_Conformal_Conic\",GEOGCS[\"WGS 84\","
                                       "DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,"
                                       "AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],"
                                       "PRIMEM[\"Greenwich\",0],UNIT[\"Degree\",0.0174532925199433],AUTHORITY["
                                       "\"EPSG\",\"4326\"]],PROJECTION[\"Lambert_Conformal_Conic_2SP\"],"
                                       "PARAMETER[\"latitude_of_origin\",40],PARAMETER[\"central_meridian\",-100],"
                                       "PARAMETER[\"standard_parallel_1\",49],PARAMETER[\"standard_parallel_2\",77],"
                                       "PARAMETER[\"false_easting\",0],PARAMETER[\"false_northing\",0],"
                                       "UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AXIS[\"Easting\",EAST],"
                                       "AXIS[\"Northing\",NORTH]]",
                          "region": "Hudson Bay",
                          "proj:bbox": [
                              39635.38409999758,
                              1165147.9602999985,
                              2687011.6921999976,
                              3743636.792300001
                          ],
                          "proj:geometry": {
                              "type": "Polygon",
                              "coordinates": [
                                  [
                                      [
                                          1049101.9816000015,
                                          1165147.9602999985
                                      ],
                                      [
                                          984834.7013999969,
                                          1241762.0366999991
                                      ],
                                      [
                                          419282.63610000163,
                                          1915965.9090000018
                                      ],
                                      [
                                          110799.69139999896,
                                          2283713.4756999984
                                      ],
                                      [
                                          39635.38409999758,
                                          2368549.6110999994
                                      ],
                                      [
                                          665210.1768999994,
                                          2893748.8044999987
                                      ],
                                      [
                                          1677552.496600002,
                                          3743636.792300001
                                      ],
                                      [
                                          1703264.5890000015,
                                          3712995.5080000013
                                      ],
                                      [
                                          1934673.420400001,
                                          3437223.949000001
                                      ],
                                      [
                                          2333210.8522000015,
                                          2962284.0418
                                      ],
                                      [
                                          2538907.5912000015,
                                          2717153.767099999
                                      ],
                                      [
                                          2616043.8682999983,
                                          2625229.914099999
                                      ],
                                      [
                                          2628899.914499998,
                                          2609909.271899998
                                      ],
                                      [
                                          2687011.6921999976,
                                          2540657.0507999994
                                      ],
                                      [
                                          1049101.9816000015,
                                          1165147.9602999985
                                      ]
                                  ]
                              ]
                          }
                      },
                      "geometry": {
                          "type": "Polygon",
                          "coordinates": [
                              [
                                  [
                                      -85.46220711823483,
                                      49.21506337964712
                                  ],
                                  [
                                      -86.0958140715453,
                                      50.01675833873254
                                  ],
                                  [
                                      -92.93457533680021,
                                      56.93624181180134
                                  ],
                                  [
                                      -97.92260693804486,
                                      60.52453185754117
                                  ],
                                  [
                                      -99.23757113710072,
                                      61.32311938824809
                                  ],
                                  [
                                      -85.0674225720189,
                                      65.45820011448673
                                  ],
                                  [
                                      -54.50984088206913,
                                      68.24374994695228
                                  ],
                                  [
                                      -54.52652058139048,
                                      67.87472836158548
                                  ],
                                  [
                                      -54.65634165293336,
                                      64.54748446004443
                                  ],
                                  [
                                      -54.81869230163133,
                                      58.81698436401498
                                  ],
                                  [
                                      -54.88228128610478,
                                      55.873517255598365
                                  ],
                                  [
                                      -54.90351606696391,
                                      54.774051631256164
                                  ],
                                  [
                                      -54.90693250241476,
                                      54.59107627703887
                                  ],
                                  [
                                      -54.921962487703226,
                                      53.76501834115755
                                  ],
                                  [
                                      -85.46220711823483,
                                      49.21506337964712
                                  ]
                              ]
                          ]
                      },
                      "links": [],
                      "assets": {
                          "data": {
                              "href": "https://ice-glaces.ec.gc.ca/www_archive/AOI_09/Coverages/rgc_a09_20201221_CEXPRHB.zip",
                              "type": "x-gis/x-shapefile"
                          }
                      },
                      "bbox": [
                          -99.23757113710072,
                          49.21506337964712,
                          -54.50984088206913,
                          68.24374994695228
                      ],
                      "stac_extensions": [
                          "projection"
                      ]
                      }
