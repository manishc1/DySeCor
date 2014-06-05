#! /usr/bin/python


from constants import *
from utils import *

import os
import xml.etree.ElementTree as ET


class Frequency_Counter(object):
    """
    Class to calculate the frequencies of words.
    """

    def __init__(self, dir_list):
        """
        Initialize the Frequency_Counter class.
        """
        self.dir_list = dir_list
        #self.total_word_frequency = {}
        #self.word_document_frequency = {}
        self.frequencies = [{}, {}]
        self.stop_words = readLines(CONFIG_DIR + '/stop_words_new.cfg')
        self.filenames = [FEATURE_DIR + '/total_words_bow.txt', FEATURE_DIR + '/word_docs_bow.txt']


    def add_to_freq(self, words, index):
        """
        Adds the words to the frequency counts.
        """
        for word in words:
            count = 0
            if (word in self.stop_words):
                continue
            if (self.frequencies[index].has_key(word)):
                count = self.frequencies[index][word] + 1
            else:
                count = 1
            self.frequencies[index][word] = count


    def read_file(self, filename):
        """
        Parses the xml files and extracts words from descriptions.
        """
        tree = ET.parse(filename)
        root = tree.getroot()
        for child in root:
            docDesc = ''
            if (child.tag == 'Description'):
                docDesc = clean(child.text)
        words = docDesc.lower().split()
        self.add_to_freq(words, 0)
        words = list(set(words))
        self.add_to_freq(words, 1)


    def traverse_dir(self):
        """
        Walks the directories.
        """
        for path, length in self.dir_list:
            count = 0
            for rootdir, _, files in os.walk(path):
                for filename in files:
                    if (filename.endswith('.xml')):
                        self.read_file(str(rootdir) + '/' + filename)
                        count = count + 1
                        if (count >= length):
                            break
                if (count >= length):
                    break

        #print self.frequencies


    def write(self):
        """
        Write to the bag of words file.
        """
        for index in range(len(self.frequencies)):
            string = ''
            frequency = sorted(self.frequencies[index].items(), key=lambda x: x[1], reverse=True)
            for key, val in frequency:
                if (is_ascii(key)):
                    string = string + str(key) + ':=' + str(val) + '\n'
            writeString(self.filenames[index], string)


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def main():
    # Clean: version to 1, only punctuation words, punctuations from words, etc.
    fc = Frequency_Counter([tuple([DATA_DIR + '/CVE', INSTANCE_FILE_LIMIT]), tuple([DATA_DIR + '/WikiArticle', INSTANCE_FILE_LIMIT])])
    fc.traverse_dir()
    fc.write()


if __name__ == "__main__":
    main()
