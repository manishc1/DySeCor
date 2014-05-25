"""
Contains all the constants.
"""

import os

XML_HEAD = '<?xml version="1.0" encoding="UTF-8"?>\n'


CONFIG_DIR = os.path.abspath(__file__ + '/../../config')
DATA_DIR = os.path.abspath(__file__ + '/../../data')
LOG_DIR =  os.path.abspath(__file__ + '/../../log')


NVD_BASE_YEAR = 2002
NVD_YEAR_RSS = 'http://nvd.nist.gov/download/nvdcve-'
NVD_RECENT_RSS = 'http://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-recent.xml'
