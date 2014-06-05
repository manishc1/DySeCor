"""
Fetches wikipedia articles for the nist glossary terms.
"""

from constants import *
from datetime import datetime
from lxml import etree
from wikiapi import WikiApi
from utils import *

import lxml.builder as lb
import sys


visited_results = []

class Glossary(object):
    """
    Class that contains the glossary.
    """

    def __init__(self, filenames):
        """
        Initialize the Glossary class.
        """
        self.filenames = filenames
        self.phrases = []
        self.get_phrases()
        self.phrases = sorted(self.phrases)


    def get_phrases(self):
        """
        Read the phrases from all the files.
        """
        for filename in self.filenames:
            print filename
            lines = readLines(filename)
            for line in lines:
                line = line.strip().lower()
                if ((len(line) > 0) and (line[0] != '#')):
                    if (line[0] == '/' and len(line.split(' ', 1)) > 1):
                        self.phrases.append(tuple([line.split(' ', 1)[1], True]))
                    else:
                        self.phrases.append(tuple([line, False]))


class WikiGrabber(object):
    """
    Class to grab the wiki articles.
    """

    def __init__(self, filenames):
        """
        Initialize the WikiGrabber class.
        """
        self.glossary = Glossary(filenames)
        self.wiki = WikiApi({})


    def get_articles(self, dir_name):
        """
        Get wiki articles for all the phrases and convert to xml.
        """
        global visited_results
        step = 1000 + len(visited_results)
        try:
            for phrase, flag in self.glossary.phrases:
                print phrase
                results = self.wiki.find(phrase)
                for result in results:
                    if (result not in visited_results):
                        article = self.wiki.get_article(result)
                        self.article_to_xml(article, flag, dir_name)
                        visited_results.append(result)
                        if (len(visited_results) > step):
                            print phrase, len(visited_results)
                            step = step + 1000
        except:
            print phrase, len(visited_results)


    def article_to_xml(self, article, flag, dir_name):
        """
        Create a xml from the article.
        """
        try:
            docId = 'Wiki_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
            docType = 'Wiki'
            docSource = 'wikipedia'
            docDate = ''
            docTitle = article.heading
            docDesc = clean(article.summary)

            if (len(docDesc.split()) < WORD_LEN_THRESHOLD):
                return 

            if (flag and ('security' not in docDesc.lower())):
                return

            document = lb.E.Document(
                lb.E.Title(docTitle),
                lb.E.Date(docDate),
                lb.E.Description(docDesc),
                id=docId, type=docType, src=docSource)		
            doc = etree.tostring(document, pretty_print=True)

            xml_filename = dir_name + docId + '.xml'
            writeString(xml_filename, XML_HEAD + doc)
        except Exception as e:
            print e


def get_security_results(filenames):
    """
    Pre-fill visited with security term results.
    """
    global visited_results

    wiki = WikiApi({})

    phrases = []
    for filename in filenames:
        lines = readLines(filename)
        for line in lines:
            line = line.strip()
            if ((len(line) > 0) and (line[0] != '#')):
                if (line[0] == '/'):
                    phrases.append(line.split(' ', 1)[1])
                else:
                    phrases.append(line)

    for phrase in phrases:
        results = wiki.find(phrase)
        for result in results:
            if (result not in visited_results):
                visited_results.append(result)
    

def main(instance_type):
    if (instance_type == 'positive'):
        filenames = [SECURITY_GLOSSARY]
        dir_name = DATA_DIR + '/WikiArticle/'
    if (instance_type == 'negative'):
        #get_security_results([SECURITY_GLOSSARY])
        #print len(visited_results)
        #filenames = COMPUTER_GLOSSARY
        filenames = [WORD_LIST]
        dir_name = NEG_DATA_DIR + '-non-CS/WikiArticle/'
    wg = WikiGrabber(filenames)
    wg.get_articles(dir_name)
    print len(visited_results)
 

if __name__=="__main__":
    nargs = len(sys.argv)
    args = sys.argv
    if nargs == 2:
        main(args[1])
    else:
        print "Usage: python wikipedia.py <'positive'/'negative'>"

