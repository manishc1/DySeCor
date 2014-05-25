#! /usr/bin/python

"""
Details to grab the NVD vulnerabilities.
"""

from constants import *
from datetime import datetime
from lxml import etree
from utils import *


import feedparser
import lxml.builder as lb
import sys, os


LOG_FILE = LOG_DIR + '/nvd.log'
CVE_DATA_DIR = DATA_DIR + '/CVE/'


def parseDateTitleDesc(post, year):
	"""
	Parse the date, title and the description.
	"""
	if year == -1:
		return post[u'vuln_published-datetime'], post[u'vuln_cve-id'], post[u'vuln_summary']

	lines = [line.strip() for line in post[u'refs'].split('\n')]
	for line in reversed(lines):
		if ((line[0:4] == str(year)) and (len(line.split(' ', 1)) > 1)):
			return line[0:4] + '-' + line[4:6] + '-' + line[6:8], line.split(' ', 1)[1], post[u'desc']
	return '', '', post[u'desc']


def parse(url, year):
	"""
	Extract all the vulnerabilities to seperate files.
	"""
	feed = feedparser.parse(url)
	for post in feed.entries:
		vulId = 'CVE_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
		vulType = 'CVE_Vulnerability'
		vulDate, vulTitle, vulDesc = parseDateTitleDesc(post, year)

		document = lb.E.Document(
			lb.E.Title(vulTitle),
			lb.E.Date(vulDate),
			lb.E.Description(vulDesc),
			id=vulId, type=vulType)		
		doc = etree.tostring(document, pretty_print=True)

		filename = CVE_DATA_DIR + vulId + '.xml'
		writeString(filename, XML_HEAD + doc)


def parseRSSList():
	"""
	Parses the rss list.
	"""
	curr_year = datetime.now().year	
	year = NVD_BASE_YEAR
	while(year <= curr_year):
		url = NVD_YEAR_RSS + str(year) + '.xml'
		try:			
			parse(url, year)
			year = year + 1
		except Exception as e:
			log = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f') + ': ' + 'Cannot parse URL: ' + url + ' : ' + str(e)
			appendString(LOG_FILE, log)
			print log

	parse(NVD_RECENT_RSS, -1)


def main():
	"""
	Main function.
	"""
	parseRSSList()


if __name__ == "__main__":
	"""
	Entry point.
	"""
	main()
