#! /usr/bin/python


from constants import *
from utils import *

import os
import xml.etree.ElementTree as ET


all_words = []
unique_words = []
all_non_stop_words = []
unique_non_stop_words = []
step = 50000
threshold = step


def read_file(filename):
    global all_words
    global unique_words
    global all_non_stop_words
    global unique_non_stop_words
    global threshold

    tree = ET.parse(filename)
    root = tree.getroot()
    for child in root:
        docTitle = ''
        docDesc = ''
        if (child.tag == 'Title'):
            docTitle = child.text
            if (docTitle is None):
                docTitle = ''
        elif (child.tag == 'Description'):
            docDesc = clean(child.text)
            if (docDesc is None):
                docDesc = ''
        words = docTitle.lower().split() + docDesc.lower().split()
        all_words = all_words + words
        unique_words = unique_words + list(set(words))
        if (len(all_words) > threshold):
            print len(all_words), len(list(set(unique_words)))
            threshold = threshold + step


def traverse_dir(path):
    for rootdir, subdir, files in os.walk(path):
        for filename in files:
            if (filename.endswith('.xml')):
                read_file(str(rootdir) + '/' + filename)

def main():
    #traverse_dir(DATA_DIR)

    stop_words = readLines(CONFIG_DIR + '/stop_words_new.cfg')
    print stop_words
    for word in all_words:
        if (word not in stop_words):
            all_non_stop_words.append(word)
    unique_non_stop_words = list(set(all_non_stop_words))

    print 'All words:', len(all_words)
    print 'Unique words:', len(list(set(unique_words)))
    print 'All Non-Stop words:', len(all_non_stop_words)
    print 'Unique Non-Stop words:', len(unique_non_stop_words)


if __name__ == "__main__":
    main()
