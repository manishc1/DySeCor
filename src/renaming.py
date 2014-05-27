#! /usr/bin/python

from constants import *
from datetime import datetime
from lxml import etree
from utils import *

import lxml.builder as lb
import os
import xml.etree.ElementTree as ET


COUNT = 97
TYPE = 'RandomArticle'
RENAME_DATA_DIR = DATA_DIR + '/' + TYPE +'/'


def main():
    for i in range(50, COUNT):
        filename = RENAME_DATA_DIR + str(i+1) + '.xml'
        tree = ET.parse(filename)
        root = tree.getroot()

        docId = TYPE + '_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
        docType = TYPE
        docSource = root.attrib['src']        
        for child in root:
            if (child.tag == 'Title'):
                docTitle = child.text
            elif (child.tag == 'Date'):
                docDate = child.text
                if (docDate is None):
                    docDate = ''
            elif (child.tag == 'Description'):
                docDesc = clean(child.text)

        document = lb.E.Document(
            lb.E.Title(docTitle),
            lb.E.Date(docDate),
            lb.E.Description(docDesc),
            id=docId, type=docType, src=docSource)		
        doc = etree.tostring(document, pretty_print=True)

        xml_filename = RENAME_DATA_DIR + docId + '.xml'
        writeString(xml_filename, XML_HEAD + doc)

        os.system('rm %(filename)s' % locals())


if __name__ == "__main__":
    main()
