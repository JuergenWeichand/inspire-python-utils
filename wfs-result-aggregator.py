#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################################
#   usage: python wfs-result-aggregator.py source_directory
#
#   description: aggregates features from multiple WFS 2.0 responses
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
    print('usage: python wfs-result-aggregator.py source_directory')
    sys.exit(1)

namespaces = { 'wfs' : 'http://www.opengis.net/wfs/2.0' }
wfs_fc = etree.Element('{http://www.opengis.net/wfs/2.0}FeatureCollection', nsmap=namespaces)
wfs_count = 0

for root, directories, filenames in os.walk(source_dir):

    for filename in filenames:
        xml_file = os.path.join(root, filename)
        if xml_file.endswith('.gml') or xml_file.endswith('.xml'):

            print ('Parsing %s' % xml_file)
            xml = etree.parse(xml_file)

            i = 0
            for wfs_member in xml.xpath('//wfs:member', namespaces=namespaces):
                wfs_fc.append(wfs_member)
                i+=1
            wfs_count+= i
            print('... %s features found.' % str(i))


wfs_fc.set('numberMatched', str(wfs_count))
wfs_fc.set('numberReturned', str(wfs_count))
doc = etree.ElementTree(wfs_fc)

target_file = os.path.join(source_dir, 'joined.gml')

print('\n' +
      'Writing %s features to file: %s' % (str(wfs_count), target_file)
        + '\n')
f = open(target_file, 'w')
doc.write(f, xml_declaration=True, encoding='utf-8')
