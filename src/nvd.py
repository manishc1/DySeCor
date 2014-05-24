#! /usr/bin/python

"""
Details to grab the NVD vulnerabilities.
"""

from constants import *
from datetime import datetime
from lxml import etree

import feedparser
import lxml.builder as lb
import sys


def parse(url):
	"""
	Extract all the vulnerabilities to seperate files.
	"""
	feed = feedparser.parse(url)
	for post in feed.entries:
		vulId = 'CVE_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
		vulType = 'CVE_Vulnerability'
		vulDate = post[u'vuln_published-datetime']
		vulTitle = post[u'vuln_cve-id']
		vulDesc = post[u'vuln_summary']

		document = lb.E.Document(
			lb.E.Title(vulTitle),
			lb.E.Date(vulDate),
			lb.E.Description(vulDesc),
			id=vulId, type=vulType)		
		doc = etree.tostring(document, pretty_print=True)

		filename = DATA_DIR + '/CVE/CVE_' + vulId + '.xml'
		writeString(filename, XML_HEAD + '\n' + doc)


def parseList(rssList):
	"""
	Parses the rss list.
	"""
	for url in rssList:
		parse(url)


def main():
	"""
	Main function.
	"""
	rssList = readLines(NVD_RSS_LIST_FILE)
	parseList(rssList)


if __name__ == "__main__":
	"""
	Entry point.
	"""
	main()
