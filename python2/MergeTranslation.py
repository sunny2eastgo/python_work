#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fnmatch
import os
import xml.etree.ElementTree as ET
import re
import csv
import tempfile
import codecs
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
print 'defaultencoding' ,sys.getdefaultencoding()

csvfiles = fnmatch.filter(os.listdir('.'), '*.txt')
for csvfile in csvfiles:
    with codecs.open(csvfile, "rb", "utf-8") as f:
        lang = re.match('(ewb_)(.+)(_utf8\.txt)', csvfile).group(2)
	if re.match('([a-z]+_)([a-z]+)', lang):
	    lang1 = re.sub('([a-z]+_)([a-z]+)', r'\1', lang)
	    lang2 = re.sub('([a-z]+_)([a-z]+)', r'\2', lang).upper()
	    lang = lang1 + lang2
        if lang:
            tsfile = 'ewb_' + lang + '.ts'
	    print tsfile
            tree = ET.parse(tsfile)
            root = tree.getroot()

            # 1st 4lines are skipped
            for i in range(4):
                f.next()

            csvReader = csv.reader(f)
            for row in csvReader:
                ts_id = row[0]
                ts_tr = row[1]
                msg = root.find(".//message[@id=\'" + ts_id + "\']")	
		if msg is not None:
		    translation = msg.find('translation')
		    tail = translation.tail
		    translation.clear()
		    translation.text = ts_tr
		    translation.tail = tail
		'''
		else:
		    context = root.find(".//context")
		    context.append
		'''

            tmpf = tempfile.TemporaryFile("rw+b")
            tree.write(tmpf, encoding="utf-8", xml_declaration=True)
            tmpf.seek(0)
            with codecs.open(tsfile, "w+b", "utf-8") as wf:
                i = 0
                for line in tmpf:
                    if i == 1:
                        wf.write("<!DOCTYPE TS>\n")
                    wf.write(line)
                    i += 1	    
