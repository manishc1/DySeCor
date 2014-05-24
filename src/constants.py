"""
Contains all the constants.
"""

import os

XML_HEAD = '<?xml version="1.0" encoding="UTF-8"?>\n'

CONFIG_DIR = os.path.abspath(__file__ + '/../../config')
DATA_DIR = os.path.abspath(__file__ + '/../../data')

NVD_RSS_LIST_FILE = CONFIG_DIR + '/nvd_rss_list.cfg'

print NVD_RSS_LIST_FILE
