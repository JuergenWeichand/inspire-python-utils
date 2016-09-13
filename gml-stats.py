#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################################
#   usage: python gml-stats.py source_directory
#
#   description: creates a simple statistic (.stat) for each gml file
#
#   requires: python-lxml
#
#   license: Apache 2.0
#
#   (c) 2016 Jürgen Weichand (weichand.de)
###########################################################################################

from lxml import etree
import os
import sys

if len(sys.argv) == 2:
    source_dir = sys.argv[1]
else:
    print('usage: python gml-stats.py source_directory')
    sys.exit(1)


namespaces = { 'wfs' : 'http://www.opengis.net/wfs/2.0' }

for root, directories, filenames in os.walk(source_dir):

    for filename in filenames:
        xml_file = os.path.join(root, filename)
        if '' in xml_file and xml_file.endswith('.gml'):

            print(xml_file)
            xml = etree.parse(xml_file)

            featurecount = {}

            for feature in xml.xpath('//wfs:member/*', namespaces=namespaces):
                feature_name = feature.xpath('local-name()')
                if feature_name in featurecount:
                    featurecount[feature_name] += 1
                else:
                    featurecount[feature_name] = 1


            f = open(xml_file + '.stat', mode='w')
            for k, v in sorted(featurecount.items()):
                    f.write('%s %s\n' % (k, v))