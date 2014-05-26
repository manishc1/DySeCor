"""
Fetches wikipedia articles for the nist glossary terms.
"""

from constants import *
from datetime import datetime
from lxml import etree
from wikiapi import WikiApi
from utils import *

import lxml.builder as lb


WIKI_DATA_DIR = DATA_DIR + '/WikiArticles/'


class Glossary(object):
    """
    Class that contains the glossary.
    """

    def __init__(self):
        """
        Initialize the Glossary class.
        """
        self.filenames = [SECURITY_GLOSSARY]
        self.phrases = []
        self.get_phrases()


    def get_phrases(self):
        """
        Read the phrases from all the files.
        """        
        for filename in self.filenames:
            lines = readLines(filename)
            for line in lines:
                line = line.strip()
                if ((len(line) > 0) and (line[0] != '#')):
                    self.phrases.append(line)


class WikiGrabber(object):
    """
    Class to grab the wiki articles.
    """

    def __init__(self):
        """
        Initialize the WikiGrabber class.
        """
        self.glossary = Glossary()
        self.wiki = WikiApi({})


    def get_articles(self):
        """
        Get wiki articles for all the phrases and convert to xml.
        """
        for phrase in self.glossary.phrases:
            results = self.wiki.find(phrase)
            for result in results:
                article = self.wiki.get_article(result)
                self.article_to_xml(article)
            break


    def article_to_xml(self, article):
        """
        Create a xml from the article.
        """
        docId = 'Wiki_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
        docType = 'Wiki'
        docSource = 'wikipedia'
        docDate = ''
        docTitle = article.heading
        docDesc = clean(article.summary)

        document = lb.E.Document(
            lb.E.Title(docTitle),
            lb.E.Date(docDate),
            lb.E.Description(docDesc),
            id=docId, type=docType, src=docSource)		
        doc = etree.tostring(document, pretty_print=True)

        xml_filename = WIKI_DATA_DIR + docId + '.xml'
        writeString(xml_filename, XML_HEAD + doc)


def main():
    wg = WikiGrabber()
    wg.get_articles()
 

if __name__=="__main__":
    main()

