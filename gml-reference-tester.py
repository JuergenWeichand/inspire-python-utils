#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################################
#   usage: python gml-reference-tester.py source_directory
#
#   description: finding unused gml references
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
    print('usage: python gml-reference-tester.py source_directory')
    sys.exit(1)

namespaces = {  'gml'  : 'http://www.opengis.net/gml/3.2',
                'xlink': 'http://www.w3.org/1999/xlink' }

for root, directories, filenames in os.walk(source_dir):

    for filename in filenames:
        xml_file = os.path.join(root, filename)
        if xml_file.endswith('.gml') or xml_file.endswith('.xml'):

            xml = etree.parse(xml_file)

            # find all xlink:href
            references = set()
            for href in xml.xpath('//@xlink:href', namespaces=namespaces):
                if not 'crs' in href: # Hack
                    if not 'inspire' in href: # Hack
                        references.add(href.split('#')[-1])

            # find all feature ids
            for gml_id in xml.xpath('//@gml:id', namespaces=namespaces):
                if gml_id in references:
                    references.remove(gml_id)

            if len(references) > 0:
                print('References without features ' + str(sorted(references)))
