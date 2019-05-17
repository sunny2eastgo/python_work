#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fnmatch
import os
import xml.etree.ElementTree as ET
import re
import tempfile
import codecs
import xml.dom.minidom as md
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
print 'defaultencoding' ,sys.getdefaultencoding()

argv = sys.argv
argc = len(argv)
if argc > 1: 
    ts_id = argv[1]
else:
    print "No message id then quit."
    quit()

tsfiles = fnmatch.filter(os.listdir('.'), '*.ts')
for tsfile in tsfiles:
    print tsfile
    tree = ET.parse(tsfile)
    root = tree.getroot()

    msg = root.find(".//message[@id=\'" + ts_id + "\']")	
    if msg is None:
	context = root.find("./context")
	message = ET.SubElement(context, 'message')
	message.set('id', ts_id)
	ET.SubElement(message, 'location')
	ET.SubElement(message, 'source')
	ET.SubElement(message, 'translation')
    else:
	print "already has this id's entry then formatting only."

    tmpf = tempfile.TemporaryFile("rw+b")
    #tree.write(tmpf, encoding="utf-8", xml_declaration=True)
    document = md.parseString(ET.tostring(root, 'utf-8'))
    document.writexml(tmpf, encoding='utf-8', newl='\n', indent='', addindent='    ')

    tmpf.seek(0)
    with codecs.open(tsfile, "w+b", "utf-8") as wf:
        i = 0
        for line in tmpf:
            if i == 1:
		wf.write("<!DOCTYPE TS>\n")
	    emptyline = line.lstrip()
	    print emptyline
            if emptyline != "":
		wf.write(line)

            i += 1	    
