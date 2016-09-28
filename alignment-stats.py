#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################################
# usage: python alignment-stats.py source_directory
#
# description: analyzes HALE-Alignments (used transformation functions)
#
# license: Apache 2.0
#
# (c) 2016 Jürgen Weichand (weichand.de)
###########################################################################################

import xml.etree.ElementTree as ET
import collections
import os
import sys
import json

if len(sys.argv) == 2:
    source_dir = sys.argv[1]
else:
    print('usage: python alignment-stats.py source_directory')
    sys.exit(1)

counter = collections.Counter()

for root, subdirs, files in os.walk(source_dir):
    for file in files:
        filename = os.path.join(root, file)
        if filename.endswith('alignment.xml'):
            print(file)
            xml = ET.parse(filename)
            alignment = xml.getroot()
            for cell in alignment.iter('{http://www.esdi-humboldt.eu/hale/alignment}cell'):
                counter[cell.get('relation')] += 1

            print(json.dumps(counter, indent=3))
            print('############################################')








