#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  Icechart STAC Service
# Purpose:  Scrape NIC and CIS web sites for ice charts
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
import datetime
from string import Template

from utility import parse_htmlform_files, test_url
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

# first available data from CIS appears to be 1968-06-25
STARTYEAR = 1968
STARTMONTH = 6
STARTDAY = 25

# define some constants for accessing the NIC website
VERIFY = True
nic_basesite = 'https://www.natice.noaa.gov/products/'
nic_basesite_new = 'https://usicecenter.gov/Products/DisplaySearchResults'
nic_ra = 'https://usicecenter.gov/Products/ArchiveSearch?table=WeeklyArctic&product=Arctic%20Weekly%20Shapefile&linkChange=arc-two'
nic_antarctic_new = 'https://usicecenter.gov/Products/ArchiveSearch?table=WeeklyAntarctic&product=Antarctic%20Weekly%20Shapefile&linkChange=ant-two'
nic_form = 'weekly_products.html'

# define some constants for accessing the CIS website
cis_searchpage = "https://iceweb1.cis.ec.gc.ca/Archive/page1.xhtml?lang=en"
cis_searchbase = "https://iceweb1.cis.ec.gc.ca/Archive/page1.xhtml"

cis_format_break = '2020-01-14'
cis_e00_baseurl = 'https://ice-glaces.ec.gc.ca/www_archive/$AOI/Coverages/rgc_$LAOI$DATE$CAOI.e00'
cis_shp_baseurl = 'https://ice-glaces.ec.gc.ca/www_archive/$AOI/Coverages/rgc_$LAOI$DATE$CAOI.zip'
aoi_list = ['AOI_09', 'AOI_10', 'AOI_11', 'AOI_12', 'AOI_13']
laoi_list = ['a09_', 'a10_', 'a11_', 'a12_', 'a13_']
caoi_list = ['CEXPRHB', 'CEXPRWA', 'CEXPREA', 'CEXPREC', 'CEXPRGL']
cis_aoi_labels = ['Hudson Bay', 'Western Arctic', 'Eastern Arctic', 'Eastern Coast', 'Great Lakes']


def gogetnicdata(site: str = 'New', startyear: int = STARTYEAR, startmonth: int = STARTMONTH, startday: int = STARTDAY):
    """ new and improved web scraping for NIC shapefiles
    returns a list of available files from the old NIC icechart server """
    # query the website for Arctic datasets between the given start date and today
    td = datetime.date.today()
    ts = datetime.date(startyear, startmonth, startday)
    target_files = []
    if site == 'New':  # use the new (Dec 2020) site
        # ssn = requests.session()
        # baseurl = 'https://usicecenter.gov/Products/ArchiveSearch'
        # qry = {'table': 'WeeklyArctic', 'product': 'Arctic%20Weekly%20Shapefile', 'linkChange': 'arc-two'}
        # frm = ssn.get(baseurl, params=qry)
        # fmr.url
        # first search the arctic (zip files only as far as I can tell)
        payload = {'searchText': 'WeeklyArctic', 'searchProduct': 'Arctic Weekly Shapefile',
                   'startDate': ts.strftime("%m/%d/%Y"), 'endDate': td.strftime("%m/%d/%Y")}
        target_files.extend(parse_htmlform_files(nic_basesite_new, '', payload, 'zip', VERIFY))
        # now search for antarctic files
        payload = {'searchText': 'WeeklyAntarctic', 'searchProduct': 'Antarctic Weekly Shapefile',
                   'startDate': ts.strftime("%m/%d/%Y"), 'endDate': td.strftime("%m/%d/%Y")}
        target_files.extend(parse_htmlform_files(nic_basesite_new, '', payload, 'zip', VERIFY))
    else:
        # first search for Arctic E00 files
        payload = {'oldarea': 'Arctic', 'oldformat': 'E00', 'year0': str(ts.year), 'month0': ts.strftime("%b"),
                   'day0': str(ts.day).zfill(2), 'year1': str(td.year), 'month1': td.strftime("%b"),
                   'day1': str(td.day).zfill(2), 'area': 'Arctic', 'format': 'E00', 'subareas': 'Hemispheric'}

        target_files.extend(parse_htmlform_files(nic_basesite, nic_form, payload, 'e00', VERIFY))
        # Now search for Arctic shapefiles
        payload['oldformat'] = 'Shapefiles'
        payload['format'] = 'Shapefiles'
        target_files.extend(parse_htmlform_files(nic_basesite, nic_form, payload, 'zip', VERIFY))

        # now do the antarctic - shapes
        payload['oldarea'] = 'Antarctic'
        payload['area'] = 'Antarctic'
        target_files.extend(parse_htmlform_files(nic_basesite, nic_form, payload, 'zip', VERIFY))
        # finally antarctic E00
        payload['oldformat'] = 'E00'
        payload['format'] = 'E00'
        target_files.extend(parse_htmlform_files(nic_basesite, nic_form, payload, 'e00', VERIFY))

    # strip off the file extension from the name column of the results
    for targ in target_files:
        targ[0] = os.path.splitext(targ[0])[0]

    return target_files


# helper functions for working with selenium
# ref:  http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 30:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )


class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)


def gogetcisdata(startyear: int = STARTYEAR, startmonth: int = STARTMONTH, startday: int = STARTDAY):
    """ retrieve a list of e00 and zip data from the CIS site
    Old data (from ??? to 01-2020) comes as an E00 file named like this: rgc_a10_20200106_CEXPRWA.e00
    new data (since 01-2020 comes as a zip file named like this:  rgc_a10_20200330_CEXPRWA.zip
        containing a shape file named like this (note the DDMMYYYY):      30032020_CEXPRWA.shp

    New attempt using Selenium to access the search form - note that the geckodriver must be installed in the path
    or this will fail
    https://github.com/mozilla/geckodriver/releases
    """
    # make sure the calling parameters are valid and convert to strings
    if startyear < STARTYEAR:
        startyear = STARTYEAR
    if startmonth < 1 or startmonth > 12:
        startmonth = STARTMONTH
    if startday < 1 or startday > 31:
        startday = STARTDAY

    s_year = str(startyear)
    s_month = "{:02d}".format(startmonth)
    s_day = "{:02d}".format(startday)

    # get the search page and fill in the form
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(cis_searchpage)

    # select e00 and shp files
    driver.find_element_by_id("j_id_26:5:j_id_28").click()
    driver.find_element_by_id("j_id_2b").click()

    # select all regions
    driver.implicitly_wait(1)  # seconds
    driver.find_element_by_id("selRgnSelId:0").click()
    driver.implicitly_wait(1)  # seconds
    driver.find_element_by_id("selRgnSelId:0").click()
    driver.implicitly_wait(1)  # seconds
    driver.find_element_by_id("j_id_2g").click()

    # set items per page to 200
    driver.implicitly_wait(1)  # seconds
    select = Select(driver.find_element_by_id('itemsperpage'))
    driver.implicitly_wait(1)  # seconds
    select.select_by_value('200')
    # do it twice, because that's how I got it to work.
    driver.implicitly_wait(1)  # seconds
    select = Select(driver.find_element_by_id('itemsperpage'))
    driver.implicitly_wait(1)  # seconds
    select.select_by_value('200')

    # set the start dates (earliest)
    # wait = WebDriverWait(driver, 10)
    # element = wait.until(EC.element_to_be_clickable((By.ID, 'fromYear')))
    driver.implicitly_wait(1)  # seconds
    select = Select(driver.find_element_by_id('fromYear'))
    select.select_by_value(s_year)
    select = Select(driver.find_element_by_id('fromMonth'))
    select.select_by_value(s_month)
    select = Select(driver.find_element_by_id('fromDay'))
    select.select_by_value(s_day)
    # do it twice, again
    driver.implicitly_wait(1)  # seconds
    select = Select(driver.find_element_by_id('fromYear'))
    select.select_by_value(s_year)
    select = Select(driver.find_element_by_id('fromMonth'))
    select.select_by_value(s_month)
    select = Select(driver.find_element_by_id('fromDay'))
    select.select_by_value(s_day)

    # do it one more time
    driver.implicitly_wait(1)  # seconds
    select = Select(driver.find_element_by_id('itemsperpage'))
    driver.implicitly_wait(1)  # seconds
    select.select_by_value('200')

    # assuming the form is filled out, click the submit button
    driver.find_element_by_id("submitBtnId").click()
    # assuming we get a search result (what if it fails?) click on the first result,
    # then click next until the results stop changing
    target_files = []
    driver.find_element_by_partial_link_text('Weekly Regional Ice Data').click()
    while True:
        try:
            lnk = driver.find_element_by_partial_link_text('View data').get_attribute('href')
        except NoSuchElementException:
            lnk = driver.find_element_by_partial_link_text('Right click').get_attribute('href')
        print(lnk)
        if len(target_files):
            if target_files[-1][1] == lnk:
                break
        target_files.append([os.path.splitext(os.path.basename(lnk))[0], lnk])
        with wait_for_page_load(driver):
            driver.find_element_by_link_text('Next').click()

    driver.close()
    print('Got {0} results'.format(len(target_files)))
    return target_files
