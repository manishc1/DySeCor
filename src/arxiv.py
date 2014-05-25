"""
Scrape the pdf papers from the arxiv.
"""

from constants import *
from datetime import datetime
from lxml import etree
from mechanize import Browser
from utils import *

import lxml.builder as lb
import re
import StringIO
import urllib


PAPER_DATA_DIR = DATA_DIR + '/Paper/'


class ArxivScraper(object):
    """
    Class that scrapes the arXiv page for pdf's.
    """

    def __init__(self):
        """
        Initialize the scraper.
        """
        self.site = ARXIV_RECENT
        #self.site = 'http://www.csee.umbc.edu/~ameyk1/'
        self.pdf_urls = []


    def scrape(self):
        """
        Opens the html page and parses the pdf links.
        """
        browser = Browser()
        browser.set_handle_robots(False)

        html = browser.open(self.site)

        lines = html.read().splitlines()

        for line in lines:
            urls = re.findall('<a href="?\'?([^"\'>]*)', line)
            for url in urls:
                if '/pdf/' in url:
                    self.pdf_urls.append(url)


    def url_to_xml(self, pdf_url):
        """
        Downloads the pdf and converts to xml.
        """
        docId = 'Paper_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
        docType = 'Paper'
        docSource = 'arxiv'
        docDate = ''
        docTitle = ''

        pdf_filename = TMP_DIR + '/' + docId + '.pdf'
        txt_filename = TMP_DIR + '/' + docId + '.txt'

        urllib.urlretrieve(pdf_url, pdf_filename)
        os.system('pdftotext %(pdf_filename)s' % locals())
        os.system('rm %(pdf_filename)s' % locals())
        docDesc = readString(txt_filename)
        os.system('rm %(txt_filename)s' % locals())

        docDesc = "".join([i for i in docDesc if 31 < ord(i) < 127])
        
        document = lb.E.Document(
            lb.E.Title(docTitle),
            lb.E.Date(docDate),
            lb.E.Description(docDesc),
            id=docId, type=docType, src=docSource)		
        doc = etree.tostring(document, pretty_print=True)

        xml_filename = PAPER_DATA_DIR + docId + '.xml'
        writeString(xml_filename, XML_HEAD + doc)


    def grab(self):
        """
        Prepares the pdf url and sends for downloading.
        """
        for url in self.pdf_urls:
            self.url_to_xml(ARXIV_DOMAIN + url + '.pdf')

        
def main():
    scraper = ArxivScraper()
    scraper.scrape()
    scraper.grab()

if __name__ == "__main__":
    main()
