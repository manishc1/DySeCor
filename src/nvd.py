#! /usr/bin/python

"""
Details to grab the NVD vulnerabilities.
"""

from constants import *
import feedparser
import lxml.builder as lb
from lxml import etree
import sys, os

DIR = os.path.abspath(os.curdir)#os.path.dirname(__file__)
#sys.path.append(os.path.realpath('..'))


def getRSSList():
	f = open(NVD_RSS_LIST, 'r')
	rssList = [line for line in f]
	f.close()
	return rssList


def parse(url):
	feed = feedparser.parse(url)
	vulId = 0	
	for post in feed.entries:
		vulId = vulId+1
		vulType = "CVE_Vulnerability"
		vulDate = post[u'vuln_published-datetime']
		vulTitle = post[u'vuln_cve-id']
		vulDesc = post[u'vuln_summary']

		nstext = "new story"
		document = lb.E.Document(
			lb.E.Title(vulTitle),
			lb.E.Date(vulDate),
			lb.E.Description(vulDesc),
			id="CVE_"+str(vulId), type=vulType)		
		doc = etree.tostring(document, pretty_print=True)

		# TODO: Resolve relative file path
		filename = DIR + '/Data/CVE/CVE_'+str(vulId)+'.xml'
		f = open(filename, 'w')
		f.write(XML_HEAD)
		f.write(doc)
		f.close()

def parseList(rssList):
	for url in rssList:
		parse(url)

def main():
	rssList = getRSSList()
	parseList(rssList)

if __name__ == "__main__":
	main()
