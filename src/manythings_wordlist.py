"""
Scrape words from www.manythings.com
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
        self.site = MANYTHINGS
        self.filename = CONFIG_DIR + '/word_list.cfg'


    def scrape(self):
        """
        Scrapes the different pages.
        """
        pages = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
        for page in pages:
            self.scrape_helper(self.site + page)


    def scrape_helper(self, url):
        """
        Scrape the page at url.
        """
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html)
        divs = soup.findAll('div', {"class":"co"})
        for div in divs:
            for li in div.findAll('li'):
                appendString(self.filename, li.text.strip() + '\n')
        

def main():
    """
    Main function.
    """
    scrapper = Scrapper()
    scrapper.scrape()


if __name__ == "__main__":
    main()
