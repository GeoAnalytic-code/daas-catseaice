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
                   "bbox": [-180, 27.7226, 180, 90],
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

CIS_EASTERNARCTIC_STAC = {"type": "Feature",
                          "stac_version": "1.0.0-beta.2",
                          "id": "rgc_a11_20201221_CEXPREA",
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
                              "region": "Eastern Arctic",
                              "proj:bbox": [
                                  -195054.16480000317,
                                  2723278.977499999,
                                  1970719.0578000024,
                                  5186460.587399997
                              ],
                              "proj:geometry": {
                                  "type": "Polygon",
                                  "coordinates": [
                                      [
                                          [
                                              412383.9780000001,
                                              2723278.977499999
                                          ],
                                          [
                                              52538.365299999714,
                                              3889459.7320999987
                                          ],
                                          [
                                              -195054.16480000317,
                                              4709454.506800003
                                          ],
                                          [
                                              798708.1512999982,
                                              5013657.031999998
                                          ],
                                          [
                                              817833.4174000025,
                                              5019507.177000001
                                          ],
                                          [
                                              836958.6834999993,
                                              5025357.321999997
                                          ],
                                          [
                                              1027446.3338999972,
                                              5083624.766000003
                                          ],
                                          [
                                              1265555.8968999982,
                                              5156459.071000002
                                          ],
                                          [
                                              1363636.7114999965,
                                              5186460.587399997
                                          ],
                                          [
                                              1836563.9338999987,
                                              3837637.5100000016
                                          ],
                                          [
                                              1970719.0578000024,
                                              3199423.0485999994
                                          ],
                                          [
                                              412383.9780000001,
                                              2723278.977499999
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
                                          -91.1707557548762,
                                          64.34164477479328
                                      ],
                                      [
                                          -98.12897015026104,
                                          75.30431891748864
                                      ],
                                      [
                                          -112.67872965304991,
                                          82.38096680323945
                                      ],
                                      [
                                          -44.077184753559465,
                                          81.93524853799956
                                      ],
                                      [
                                          -43.06346660279493,
                                          81.83938218636767
                                      ],
                                      [
                                          -42.07130343577601,
                                          81.74116713354071
                                      ],
                                      [
                                          -33.3071717374462,
                                          80.64843992473486
                                      ],
                                      [
                                          -24.82217077594718,
                                          79.04878503360547
                                      ],
                                      [
                                          -21.96924552899297,
                                          78.33252005178866
                                      ],
                                      [
                                          -50.05767591097339,
                                          67.8777546586646
                                      ],
                                      [
                                          -57.23525708273641,
                                          62.64083386314862
                                      ],
                                      [
                                          -91.1707557548762,
                                          64.34164477479328
                                      ]
                                  ]
                              ]
                          },
                          "links": [],
                          "assets": {
                              "data": {
                                  "href": "https://ice-glaces.ec.gc.ca/www_archive/AOI_11/Coverages"
                                          "/rgc_a11_20201221_CEXPREA.zip",
                                  "type": "x-gis/x-shapefile"
                              }
                          },
                          "bbox": [
                              -112.67872965304991,
                              62.64083386314862,
                              -21.96924552899297,
                              82.38096680323945
                          ],
                          "stac_extensions": [
                              "projection"
                          ]
                          }

CIS_WESTERNARCTIC_STAC = {"type": "Feature",
                          "stac_version": "1.0.0-beta.2",
                          "id": "rgc_a10_20201221_CEXPRWA",
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
                              "region": "Western Arctic",
                              "proj:bbox": [
                                  -1869825.2287000008,
                                  2925058.489,
                                  265857.87569999695,
                                  4492803.5022
                              ],
                              "proj:geometry": {
                                  "type": "Polygon",
                                  "coordinates": [
                                      [
                                          [
                                              -1869802.2133999988,
                                              2925058.489
                                          ],
                                          [
                                              -1869825.2287000008,
                                              4492745.1554000005
                                          ],
                                          [
                                              -1605087.0590999983,
                                              4492753.098200001
                                          ],
                                          [
                                              -1185087.0593000017,
                                              4492765.699200001
                                          ],
                                          [
                                              74912.940200001,
                                              4492803.5022
                                          ],
                                          [
                                              170596.59000000358,
                                              4492799.1285
                                          ],
                                          [
                                              265847.91529999673,
                                              4383143.469300002
                                          ],
                                          [
                                              265851.74909999967,
                                              4266332.1657
                                          ],
                                          [
                                              265856.59160000086,
                                              3644998.874499999
                                          ],
                                          [
                                              265857.39890000224,
                                              3493755.0271000005
                                          ],
                                          [
                                              265857.6547999978,
                                              3445798.874499999
                                          ],
                                          [
                                              265857.87569999695,
                                              3398126.071899999
                                          ],
                                          [
                                              265857.75620000064,
                                              3145148.2423
                                          ],
                                          [
                                              265857.66170000285,
                                              2945148.2423
                                          ],
                                          [
                                              265857.6521999985,
                                              2925148.2423
                                          ],
                                          [
                                              250197.7846999988,
                                              2925147.5841000006
                                          ],
                                          [
                                              -29802.215000003576,
                                              2925135.8167999983
                                          ],
                                          [
                                              -1209802.2140000015,
                                              2925086.2261000015
                                          ],
                                          [
                                              -1309802.2138999999,
                                              2925082.023499999
                                          ],
                                          [
                                              -1509802.2137000002,
                                              2925073.6182999983
                                          ],
                                          [
                                              -1809802.2133999988,
                                              2925061.010499999
                                          ],
                                          [
                                              -1869802.2133999988,
                                              2925058.489
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
                                          -137.98160511005932,
                                          61.15006417855897
                                      ],
                                      [
                                          -164.0500150152319,
                                          71.42574213157417
                                      ],
                                      [
                                          -159.5322264566323,
                                          73.42446127375021
                                      ],
                                      [
                                          -150.032800920258,
                                          76.31724036580485
                                      ],
                                      [
                                          -95.9748134005946,
                                          80.6564251367662
                                      ],
                                      [
                                          -90.88428959777761,
                                          80.57025560342986
                                      ],
                                      [
                                          -87.09086361115006,
                                          79.47881612750918
                                      ],
                                      [
                                          -88.13543604847686,
                                          78.46546426927009
                                      ],
                                      [
                                          -91.71703986164682,
                                          72.93366431159826
                                      ],
                                      [
                                          -92.2855218526842,
                                          71.56177358677301
                                      ],
                                      [
                                          -92.44990265328924,
                                          71.12533327546208
                                      ],
                                      [
                                          -92.60654419806814,
                                          70.6908573512455
                                      ],
                                      [
                                          -93.34018410936865,
                                          68.37665619668807
                                      ],
                                      [
                                          -93.82493172976193,
                                          66.53934276546654
                                      ],
                                      [
                                          -93.86956533458095,
                                          66.35534384969216
                                      ],
                                      [
                                          -94.22862888587765,
                                          66.36886133020585
                                      ],
                                      [
                                          -100.68931760844269,
                                          66.4722531386356
                                      ],
                                      [
                                          -126.36208649975995,
                                          64.1206630723817
                                      ],
                                      [
                                          -128.2737778572948,
                                          63.73528523375773
                                      ],
                                      [
                                          -131.93670958574236,
                                          62.89133359011205
                                      ],
                                      [
                                          -137.0229391190495,
                                          61.458514477850656
                                      ],
                                      [
                                          -137.98160511005932,
                                          61.15006417855897
                                      ]
                                  ]
                              ]
                          },
                          "links": [],
                          "assets": {
                              "data": {
                                  "href": "https://ice-glaces.ec.gc.ca/www_archive/AOI_10/Coverages"
                                          "/rgc_a10_20201221_CEXPRWA.zip",
                                  "type": "x-gis/x-shapefile"
                              }
                          },
                          "bbox": [
                              -164.0500150152319,
                              61.15006417855897,
                              -87.09086361115006,
                              80.6564251367662
                          ],
                          "stac_extensions": [
                              "projection"
                          ]
                          }

CIS_EASTERNCOAST_STAC = {"type": "Feature",
                         "stac_version": "1.0.0-beta.2",
                         "id": "rgc_a12_20201221_CEXPREC",
                         "properties": {
                             "datetime": "2020-12-21T00:00:00Z",
                             "collection": "CIS_Ice_Charts",
                             "proj:epsg": None,
                             "proj:wkt2": "PROJCS[\"WGS_1984_Lambert_Conformal_Conic\",GEOGCS[\"WGS 84\","
                                          "DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY["
                                          "\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0],"
                                          "UNIT[\"Degree\",0.0174532925199433],AUTHORITY[\"EPSG\",\"4326\"]],PROJECTION["
                                          "\"Lambert_Conformal_Conic_2SP\"],PARAMETER[\"latitude_of_origin\",40],"
                                          "PARAMETER[\"central_meridian\",-100],PARAMETER[\"standard_parallel_1\",49],"
                                          "PARAMETER[\"standard_parallel_2\",77],PARAMETER[\"false_easting\",0],"
                                          "PARAMETER[\"false_northing\",0],UNIT[\"metre\",1,AUTHORITY[\"EPSG\","
                                          "\"9001\"]],AXIS[\"Easting\",EAST],AXIS[\"Northing\",NORTH]]",
                             "region": "Eastern Coast",
                             "proj:bbox": [
                                 1458439.2569999993,
                                 821580.7221999988,
                                 4176441.9384000003,
                                 3433997.452399999
                             ],
                             "proj:geometry": {
                                 "type": "Polygon",
                                 "coordinates": [
                                     [
                                         [
                                             2438418.606899999,
                                             821580.7221999988
                                         ],
                                         [
                                             2340192.4224999994,
                                             948773.1473000012
                                         ],
                                         [
                                             1458439.2569999993,
                                             2170920.464400001
                                         ],
                                         [
                                             3212816.791199997,
                                             3433997.452399999
                                         ],
                                         [
                                             3224500.4408000037,
                                             3417765.0053999983
                                         ],
                                         [
                                             3271235.038900003,
                                             3352835.217700001
                                         ],
                                         [
                                             3621744.5248000026,
                                             2865861.8095000014
                                         ],
                                         [
                                             3972254.0107000023,
                                             2378888.401299998
                                         ],
                                         [
                                             4089090.5059999973,
                                             2216563.9318999983
                                         ],
                                         [
                                             4170876.052699998,
                                             2102936.8033000007
                                         ],
                                         [
                                             4176441.9384000003,
                                             2095203.950199999
                                         ],
                                         [
                                             2438418.606899999,
                                             821580.7221999988
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
                                         -70.38652198391794,
                                         42.11091628696807
                                     ],
                                     [
                                         -70.75642163987577,
                                         43.49054291824594
                                     ],
                                     [
                                         -74.91351570806856,
                                         56.81556660731795
                                     ],
                                     [
                                         -38.827617249581365,
                                         55.69820396583653
                                     ],
                                     [
                                         -38.934748650875804,
                                         55.52514614747253
                                     ],
                                     [
                                         -39.353184358861036,
                                         54.8325835911761
                                     ],
                                     [
                                         -42.0489520693667,
                                         49.63643198596662
                                     ],
                                     [
                                         -44.143847864332464,
                                         44.47785919519009
                                     ],
                                     [
                                         -44.741383639947735,
                                         42.77499770695827
                                     ],
                                     [
                                         -45.134540094913305,
                                         41.58933019674084
                                     ],
                                     [
                                         -45.16058984672398,
                                         41.508843347704776
                                     ],
                                     [
                                         -70.38652198391794,
                                         42.11091628696807
                                     ]
                                 ]
                             ]
                         },
                         "links": [],
                         "assets": {
                             "data": {
                                 "href": "https://ice-glaces.ec.gc.ca/www_archive/AOI_12/Coverages/rgc_a12_20201221_CEXPREC.zip",
                                 "type": "x-gis/x-shapefile"
                             }
                         },
                         "bbox": [
                             -74.91351570806856,
                             41.508843347704776,
                             -38.827617249581365,
                             56.81556660731795
                         ],
                         "stac_extensions": [
                             "projection"
                         ]
                         }

CIS_GREATLAKES_STAC = {"type": "Feature",
                       "stac_version": "1.0.0-beta.2",
                       "id": "rgc_a13_20201221_CEXPRGL",
                       "properties": {
                           "datetime": "2020-12-21T00:00:00Z",
                           "collection": "CIS_Ice_Charts",
                           "proj:epsg": None,
                           "proj:wkt2": "PROJCS[\"WGS_1984_Lambert_Conformal_Conic\",GEOGCS[\"WGS 84\","
                                        "DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,"
                                        "AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],"
                                        "PRIMEM[\"Greenwich\",0],UNIT[\"Degree\",0.0174532925199433],"
                                        "AUTHORITY[\"EPSG\",\"4326\"]],PROJECTION[\"Lambert_Conformal_Conic_2SP\"],"
                                        "PARAMETER[\"latitude_of_origin\",40],PARAMETER[\"central_meridian\",-100],"
                                        "PARAMETER[\"standard_parallel_1\",49],PARAMETER[\"standard_parallel_2\",77],"
                                        "PARAMETER[\"false_easting\",0],PARAMETER[\"false_northing\",0],"
                                        "UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AXIS[\"Easting\",EAST],"
                                        "AXIS[\"Northing\",NORTH]]",
                           "region": "Great Lakes",
                           "proj:bbox": [
                               312729.02610000223,
                               -17853.556099999696,
                               2187460.265299998,
                               1568804.5388000011
                           ],
                           "proj:geometry": {
                               "type": "Polygon",
                               "coordinates": [
                                   [
                                       [
                                           650147.4862999991,
                                           -17853.556099999696
                                       ],
                                       [
                                           312729.02610000223,
                                           1177331.5399000011
                                       ],
                                       [
                                           1918613.2141999975,
                                           1568804.5388000011
                                       ],
                                       [
                                           2187460.265299998,
                                           464505.2776999995
                                       ],
                                       [
                                           1992607.0653000027,
                                           314791.61360000074
                                       ],
                                       [
                                           650147.4862999991,
                                           -17853.556099999696
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
                                       -92.7672507517419,
                                       39.52776791241336
                                   ],
                                   [
                                       -95.58448470223105,
                                       50.312768022080256
                                   ],
                                   [
                                       -72.1974532327571,
                                       50.09791155214823
                                   ],
                                   [
                                       -74.71825040338022,
                                       40.206664945291166
                                   ],
                                   [
                                       -77.36193459680642,
                                       39.62462756701477
                                   ],
                                   [
                                       -92.7672507517419,
                                       39.52776791241336
                                   ]
                               ]
                           ]
                       },
                       "links": [],
                       "assets": {
                           "data": {
                               "href": "https://ice-glaces.ec.gc.ca/www_archive/AOI_13/Coverages/rgc_a13_20201221_CEXPRGL.zip",
                               "type": "x-gis/x-shapefile"
                           }
                       },
                       "bbox": [
                           -95.58448470223105,
                           39.52776791241336,
                           -72.1974532327571,
                           50.312768022080256
                       ],
                       "stac_extensions": [
                           "projection"
                       ]
                       }
