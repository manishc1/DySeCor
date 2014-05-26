#! /usr/bin/env python
"""
This module provides classes for querying Google Scholar and parsing
returned results. It currently *only* processes the first results
page. It is not a recursive crawler.
"""

from constants import *
from datetime import datetime
from lxml import etree
from utils import *

import lxml.builder as lb
import optparse
import os
import sys
import re
import unicodedata


try:
    # Try importing for Python 3
    # pylint: disable-msg=F0401
    # pylint: disable-msg=E0611
    from urllib.request import HTTPCookieProcessor, Request, build_opener
    from urllib.parse import quote
    from http.cookiejar import MozillaCookieJar
except ImportError:
    # Fallback for Python 2
    from urllib2 import Request, build_opener, HTTPCookieProcessor
    from urllib import quote
    from cookielib import MozillaCookieJar

# Import BeautifulSoup -- try 4 first, fall back to older
try:
    from bs4 import BeautifulSoup
except ImportError:
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        print('We need BeautifulSoup, sorry...')
        sys.exit(1)

# Support unicode in both Python 2 and 3. In Python 3, unicode is str.
if sys.version_info[0] == 3:
    unicode = str # pylint: disable-msg=W0622
    encode = lambda s: s # pylint: disable-msg=C0103
else:
    encode = lambda s: s.encode('utf-8') # pylint: disable-msg=C0103


articles = []
PAPER_DATA_DIR = DATA_DIR + '/Paper/'


class ScholarConf(object):
    """Helper class for global settings."""

    MAX_PAGE_RESULTS = 5 # Current maximum for per-page results
    SCHOLAR_SITE = 'http://scholar.google.com'

    # USER_AGENT = 'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9.2.9) Gecko/20100913 Firefox/3.6.9'
    # Let's update at this point (3/14):
    # USER_AGENT = 'Opera/9.25 (Windows NT 5.1; U; en)'
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'

    # If set, we will use this file to read/save cookies to enable
    # cookie use across sessions.
    COOKIE_JAR_FILE = None


class ScholarArticle(object):
    """
    A class representing articles listed on Google Scholar.  The class
    provides basic dictionary-like behavior.
    """
    def __init__(self):
        self.attrs = {
            'title':         [None, 'Title',          0],
            'url':           [None, 'URL',            1],
            'year':          [None, 'Year',           2],
            'url_pdf':       [None, 'PDF link',       6],
        }


    def __getitem__(self, key):
        if key in self.attrs:
            return self.attrs[key][0]
        return None

    def __len__(self):
        return len(self.attrs)

    def __setitem__(self, key, item):
        if key in self.attrs:
            self.attrs[key][0] = item
        else:
            self.attrs[key] = [item, key, len(self.attrs)]

    def __delitem__(self, key):
        if key in self.attrs:
            del self.attrs[key]


class ScholarArticleParser(object):
    """
    ScholarArticleParser can parse HTML document strings obtained from
    Google Scholar. This is a base class; concrete implementations
    adapting to tweaks made by Google over time follow below.
    """
    def __init__(self, site=None):
        self.soup = None
        self.article = None
        self.site = site or ScholarConf.SCHOLAR_SITE
        self.year_re = re.compile(r'\b(?:20|19)\d{2}\b')

    def handle_article(self, art):
        """
        The parser invokes this callback on each article parsed
        successfully.  In this base class, the callback does nothing.
        """

    def parse(self, html):
        """
        This method initiates parsing of HTML content, cleans resulting
        content as needed, and notifies the parser instance of
        resulting instances via the handle_article callback.
        """
        print 'there'
        self.soup = BeautifulSoup(html)
        for div in self.soup.findAll(ScholarArticleParser._tag_checker):
            self._parse_article(div)
            self._clean_article()
            if self.article['title']:
                self.handle_article(self.article)

    def _clean_article(self):
        """
        This gets invoked after we have parsed an article, to do any
        needed cleanup/polishing before we hand off the resulting
        article.
        """
        if self.article['title']:
            self.article['title'] = self.article['title'].strip()

    def _parse_article(self, div):
        self.article = ScholarArticle()

        for tag in div:
            if not hasattr(tag, 'name'):
                continue

            if tag.name == 'div' and self._tag_has_class(tag, 'gs_rt') and \
                    tag.h3 and tag.h3.a:
                self.article['title'] = ''.join(tag.h3.a.findAll(text=True))
                self.article['url'] = self._path2url(tag.h3.a['href'])
                if self.article['url'].endswith('.pdf'):
                    self.article['url_pdf'] = self.article['url']
                    attr = {'title': self.article['title'], 'year': self.article['year'], 'pdf_url': self.article['url_pdf']}
                    articles.append(attr)

            if tag.name == 'font':
                for tag2 in tag:
                    if not hasattr(tag2, 'name'):
                        continue
                    if tag2.name == 'span' and \
                       self._tag_has_class(tag2, 'gs_fl'):
                        self._parse_links(tag2)

    def _parse_links(self, span):
        for tag in span:
            if not hasattr(tag, 'name'):
                continue
            if tag.name != 'a' or tag.get('href') is None:
                continue


    @staticmethod
    def _tag_has_class(tag, klass):

        """
        This predicate function checks whether a BeatifulSoup Tag instance
        has a class attribute.
        """
        res = tag.get('class') or []
        if type(res) != list:
            # BeautifulSoup 3 can return e.g. 'gs_md_wp gs_ttss',
            # so split -- conveniently produces a list in any case
            res = res.split()
        return klass in res

    @staticmethod
    def _tag_checker(tag):
        return tag.name == 'div' and ScholarArticleParser._tag_has_class(tag, 'gs_r')

    @staticmethod
    def _as_int(obj):
        try:
            return int(obj)
        except ValueError:
            return None

    def _path2url(self, path):
        """Helper, returns full URL in case path isn't one."""
        if path.startswith('http://'):
            return path
        if not path.startswith('/'):
            path = '/' + path
        return self.site + path

    def _strip_url_arg(self, arg, url):
        """Helper, removes a URL-encoded argument, if present."""
        parts = url.split('?', 1)
        if len(parts) != 2:
            return url
        res = []
        for part in parts[1].split('&'):
            if not part.startswith(arg + '='):
                res.append(part)
        return parts[0] + '?' + '&'.join(res)


class ScholarArticleParser120726(ScholarArticleParser):
    """
    This class reflects update to the Scholar results page layout that
    Google made 07/26/12.
    """
    def _parse_article(self, div):
        print 'here'
        self.article = ScholarArticle()

        for tag in div:
            if not hasattr(tag, 'name'):
                continue
            if str(tag).lower().find('.pdf'):
                if tag.find('div', {'class': 'gs_ttss'}):
                    print 'got it'
                    self._parse_links(tag.find('div', {'class': 'gs_ttss'}))

            if tag.name == 'div' and self._tag_has_class(tag, 'gs_ri'):

                if tag.find('div', {'class': 'gs_a'}):
                    year = self.year_re.findall(tag.find('div', {'class': 'gs_a'}).text)
                    self.article['year'] = year[0] if len(year) > 0 else None

                try:
                    atag = tag.h3.a
                    self.article['title'] = ''.join(atag.findAll(text=True))
                    self.article['url'] = self._path2url(atag['href'])
                    if self.article['url'].endswith('.pdf'):
                        self.article['url_pdf'] = self.article['url']
                        attr = {'title': self.article['title'], 'year': self.article['year'], 'pdf_url': self.article['url_pdf']}
                        articles.append(attr)
                except:
                    for span in tag.h3.findAll(name='span'):
                        span.clear()
                    self.article['title'] = ''.join(tag.h3.findAll(text=True))

                if tag.find('div', {'class': 'gs_fl'}):
                    self._parse_links(tag.find('div', {'class': 'gs_fl'}))


class ScholarQuery(object):
    """
    This version represents the search query parameters the user can
    configure on the Scholar website, in the advanced search options.
    """
    SCHOLAR_QUERY_URL = ScholarConf.SCHOLAR_SITE + '/scholar?' \
        + 'as_q=%(words)s' \
        + '&as_epq=%(phrase)s' \
        + '&as_oq=%(words_some)s' \
        + '&as_eq=%(words_none)s' \
        + '&as_occt=%(scope)s' \
        + '&btnG=&hl=en&as_sdt=0,5&num=%(num)s'

    def __init__(self):
        self.url = None
        self.num_results = ScholarConf.MAX_PAGE_RESULTS
        self.words = None # The default search behavior
        self.words_some = None # At least one of those words
        self.words_none = None # None of these words
        self.phrase = None
        self.scope_title = False # If True, search in title only

    def set_num_page_results(self, num_page_results):
        self.num_results = num_page_results

    def set_words(self, words):
        """Sets words that *all* must be found in the result."""
        self.words = words

    def set_words_some(self, words):
        """Sets words of which *at least one* must be found in result."""
        self.words_some = words

    def set_words_none(self, words):
        """Sets words of which *none* must be found in the result."""
        self.words_none = words

    def set_phrase(self, phrase):
        """Sets phrase that must be found in the result exactly."""
        self.phrase = phrase

    def set_scope(self, title_only):
        """
        Sets Boolean indicating whether to search entire article or title
        only.
        """
        self.scope_title = title_only

    def get_url(self):
        urlargs = {'words': self.words or '',
                   'words_some': self.words_some or '',
                   'words_none': self.words_none or '',
                   'phrase': self.phrase or '',
                   'scope': 'title' if self.scope_title else 'any',
                   'num': self.num_results or ScholarConf.MAX_PAGE_RESULTS}

        for key, val in urlargs.items():
            urlargs[key] = quote(str(val))

        return self.SCHOLAR_QUERY_URL % urlargs


class ScholarQuerier(object):
    """
    ScholarQuerier instances can conduct a search on Google Scholar
    with subsequent parsing of the resulting HTML content.  The
    articles found are collected in the articles member, a list of
    ScholarArticle instances.
    """

    class Parser(ScholarArticleParser120726):
        def __init__(self, querier):
            ScholarArticleParser120726.__init__(self)
            self.querier = querier

        def handle_article(self, art):
            self.querier.add_article(art)

    def __init__(self):
        self.articles = []
        self.query = None
        self.opener = build_opener()#HTTPCookieProcessor(MozillaCookieJar()))


    def send_query(self, query):
        """
        This method initiates a search query (a ScholarQuery instance)
        with subsequent parsing of the response.
        """
        self.clear_articles()
        self.query = query

        html = self._get_http_response(url=query.get_url())
        if html is None:
            return

        self.parse(html)


    def parse(self, html):
        """
        This method allows parsing of provided HTML content.
        """
        print 'parse'
        parser = self.Parser(self)
        parser.parse(html)

    def add_article(self, art):
        self.articles.append(art)

    def clear_articles(self):
        """Clears any existing articles stored from previous queries."""
        self.articles = []


    def _get_http_response(self, url):
        """
        Helper method, sends HTTP request and returns response payload.
        """
        try:
            print '1'
            req = Request(url=url, headers={'User-Agent': ScholarConf.USER_AGENT})
            print '2'
            hdl = self.opener.open(req)
            print '3'
            html = hdl.read()
            print '4'
            return html
        except Exception as err:
            print 'Exception: ' + str(err)
            return None


def article_to_xml(article):
    """
    Downloads the pdf and converts to xml.
    """
    docId = 'Paper_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
    docType = 'Paper'
    docSource = 'google-scholar'
    docDate = article['year']
    docTitle = article['title']

    pdf_filename = TMP_DIR + '/' + docId + '.pdf'
    txt_filename = TMP_DIR + '/' + docId + '.txt'
    pdf_url = article['pdf_url']

    print pdf_url

    os.system('wget %(pdf_url)s -O %(pdf_filename)s > /dev/null 2>&1' % locals())
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


def get_papers(phrase):
    """
    Method to form the query and get the articles.
    """
    query = ScholarQuery()    

    #query.set_words(options.allw)
    query.set_words_some(phrase)
    #query.set_words_none(options.none)
    #query.set_phrase(phrase)

    #query.set_scope(True)
    query.set_scope(False)

    query.set_num_page_results(20)

    querier = ScholarQuerier()
    querier.send_query(query)

    for article in articles:
        article_to_xml(article)


def main():
    """lines = readLines(SECURITY_GLOSSARY)
    for line in lines:
        line = line.strip()
        if ((len(line) > 1) and (line[0] != '#')):
            print line
            articles = []
            get_papers(line)
    """
    #get_papers('Ad Hoc Network')
    get_papers('cybersecurity')

if __name__ == "__main__":
    sys.exit(main())
