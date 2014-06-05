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
import sys
import urllib


class ArxivScraper(object):
    """
    Class that scrapes the arXiv page for pdf's.
    """

    def __init__(self):
        """
        Initialize the scraper.
        """
        #self.site = ARXIV_RECENT
        self.site = 'http://arxiv.org/list/cs.CL/recent'
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


    def url_to_xml(self, pdf_url, dir_name):
        """
        Downloads the pdf and converts to xml.
        """
        try:
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
            docDesc = clean(readString(txt_filename))
            os.system('rm %(txt_filename)s' % locals())

            docDesc = "".join([i for i in docDesc if 31 < ord(i) < 127])
        
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


    def grab(self, dir_name):
        """
        Prepares the pdf url and sends for downloading.
        """
        for url in self.pdf_urls:
            self.url_to_xml(ARXIV_DOMAIN + url + '.pdf', dir_name)

        
def main(instance_type):
    if (instance_type == 'positive'):
        dir_name = DATA_DIR + '/Paper-Arxiv/'
    if (instance_type == 'negative'):
        dir_name = NEG_DATA_DIR + '/Paper-Arxiv/'
    scraper = ArxivScraper()
    scraper.scrape()
    scraper.grab(dir_name)

if __name__ == "__main__":
    nargs = len(sys.argv)
    args = sys.argv
    if nargs == 2:
        main(args[1])
