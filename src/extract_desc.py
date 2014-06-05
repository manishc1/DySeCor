#! /usr/bin/python


from constants import *
from utils import *

import os
import xml.etree.ElementTree as ET


def read_file(filename):
    """
    Parse the .xml
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    for child in root:
        docDesc = ''
        if (child.tag == 'Description'):
            docDesc = clean(child.text)
            if (docDesc is None):
                docDesc = ''
    return docDesc.lower()


def traverse_dir(path):
    """
    Traverse the dir.
    """
    for rootdir, _, files in os.walk(path):
        for filename in files:
            if (filename.endswith('.xml')):
                string = read_file(str(rootdir) + '/' + filename)
                writeString(RAW_DATA_DIR + '/CVE/' + filename.replace('.xml', '.txt'), string)


def main():
    traverse_dir(DATA_DIR + '/CVE')


if __name__ == "__main__":
    main()
