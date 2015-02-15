#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 3 Assignment"""


# from datetime import datetime
import urllib2
import csv
import argparse
import sys
import re

# http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv

parser = argparse.ArgumentParser()
parser.add_argument('--url', help='display a url with a csv')
args = parser.parse_args()


def downloadData(url=''):
    '''
    Takes in a string of url and returns info from it.
    '''
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    return response


def processData(info):
    '''
    Takes in CSV and finds percentage of images hits and
    most popular browser for the day.
    '''
    csvFile = csv.reader(info)
    imageHits = 0.0
    totalHits = 0.0

    safari = 0
    chrome = 0
    firefox = 0
    ie = 0
    # other = 0


    for row in csvFile:
        path = row[0]
        # timeAccessed = row[1]
        browser = row[2]
        # status = row[3]
        # size = row[4]

        totalHits += 1.0

        images = re.search('(\.jpg|\.jpeg|\.png|\.gif)$', path, re.I)
        if images:
            imageHits += 1.0
        else:
            continue

        fsafari = re.findall('safari/\d+', browser, re.I)
        fchrome = re.findall('chrome/\d+', browser, re.I)
        ffirefox = re.findall('firefox/\d+', browser, re.I)
        fie = re.findall('MSIE\s', browser, re.I)

        if fchrome:
            chrome += 1
        elif fie:
            ie += 1
        elif ffirefox:
            firefox += 1
        elif fsafari and not fchrome is True:
            safari += 1
        else:
            other += 1

    allB = {
        'Chrome': chrome,
        'Safari': safari,
        'Internet Explorer':ie,
        'Firefox': firefox}
    # print allB

    percent = (imageHits/totalHits) * 100
    print "Image requests account for {0:0.1f} of all requests".format(percent)
    print "The most popular browser today was", max(allB, key=allB.get)

if not args.url:
    sys.exit()
else:
    try:
        csvData = downloadData(args.url)
        print processData(csvData)
    except urllib2.URLError:
        sys.exit()