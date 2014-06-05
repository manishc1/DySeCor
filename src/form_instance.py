#! /usr/bin/python

from constants import *
from utils import *

import sys
import xml.etree.ElementTree as ET


class Instance_Creator(object):
    """
    Class to form the instance.
    """

    def __init__(self, bow_File):
        """
        Initialize the class.
        """
        self.words = []
        lines = readLines(bow_File)
        for line in lines:
            if (':=' in line):
                self.words.append(line.split(':=')[0])
        self.length = len(self.words)


    def create(self, filename):
        """
        Create the instance.
        """
        instance = [0] * self.length
        tree = ET.parse(filename)
        root = tree.getroot()
        for child in root:
            docDesc = ''
            if (child.tag == 'Description'):
                docDesc = clean(child.text)
        words = docDesc.lower().split()
        for word in words:
            if (word in self.words):
                index = self.words.index(word)
                instance[index] = 1
        return instance


class ARFF_Creator(object):
    """
    Class to for the .arff file
    """

    def __init__(self, bow_file):
        """
        Initialize the class.
        """
        self.bow_file = bow_file
        self.ic = Instance_Creator(self.bow_file)


    def get_attribute_str(self):
        """
        Creates attribute_str for arff.
        """
        string = ''
        for i in range(self.ic.length):
            string = string + "@attribute 'word" + str(i+1) + "' {0 , 1}\n"
        string = string + "@attribute 'class' {positive , negative}\n"
        return string


    def create(self, dir_list):
        """
        Create the .arff file
        """
        string = '@relation sec_classify\n'
        string = string + self.get_attribute_str()
        string = string + '@data\n'
        for path, length, label in dir_list:
            count = 0
            for rootdir, _, files in os.walk(path):
                for filename in files:
                    if (filename.endswith('.xml')):
                        instance = self.ic.create(str(rootdir) + '/' + filename)
                        string = string + ','.join(str(i) for i in instance) + ',' + label + '\n'
                        count = count + 1
                        if (count >= length):
                            break
                if (count >= length):
                    break

        writeString(FEATURE_DIR + '/CVE-Wiki-WordDoc-1000.arff', string)


def main():
    """
    Entry point.
    """
    #ac = ARFF_Creator(FEATURE_DIR + '/total_words_bow.txt')
    ac = ARFF_Creator(FEATURE_DIR + '/word_docs_bow.txt')
    ac.create([tuple([DATA_DIR + '/CVE', INSTANCE_FILE_LIMIT, 'positive']), tuple([DATA_DIR + '/WikiArticle', INSTANCE_FILE_LIMIT, 'negative'])])


if __name__=="__main__":
    main()
