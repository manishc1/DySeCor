"""
Scrape computer terms from www.computerhope.com
"""

from bs4 import BeautifulSoup
from constants import *
from utils import *


import urllib2


class Scrapper(object):
    """
    Class to scrape the website.
    """

    def __init__(self):
        """
        Initialize the scrapper class.
        """
        self.site = COMPUTER_HOPE
        self.filename = CONFIG_DIR + '/computer_science_terms-4.cfg'


    def scrape(self):
        """
        Scrapes the different pages.
        """
        pages = ['num', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        for page in pages:
            self.scrape_helper(self.site + page + '.htm')


    def scrape_helper(self, url):
        """
        Scrape the page at url.
        """
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html)
        paras = soup.findAll('p', {"class":"dd"})
        for para in paras:
            for a in para.findAll('a'):
                appendString(self.filename, a.text.strip() + '\n')
        

def main():
    """
    Main function.
    """
    scrapper = Scrapper()
    scrapper.scrape()


if __name__ == "__main__":
    main()
