"""
Contains all the constants.
"""

import os

XML_HEAD = '<?xml version="1.0" encoding="UTF-8"?>\n'


CONFIG_DIR = os.path.abspath(__file__ + '/../../config')
DATA_DIR = os.path.abspath(__file__ + '/../../data/data-positive')
NEG_DATA_DIR = os.path.abspath(__file__ + '/../../data/data-negative')
LOG_DIR =  os.path.abspath(__file__ + '/../../log')
TMP_DIR =  os.path.abspath(__file__ + '/../../tmp')
FEATURE_DIR = os.path.abspath(__file__ + '/../../feature-data')
RAW_DATA_DIR = os.path.abspath(__file__ + '/../../raw-data')

NVD_BASE_YEAR = 2002
NVD_YEAR_RSS = 'http://nvd.nist.gov/download/nvdcve-'
NVD_RECENT_RSS = 'http://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-recent.xml'


COMPUTER_GLOSSARY = [CONFIG_DIR + '/computer_science_terms-1.cfg', CONFIG_DIR + '/computer_science_terms-2.cfg', CONFIG_DIR + '/computer_science_terms-3.cfg', CONFIG_DIR + '/computer_science_terms-4.cfg']
SECURITY_GLOSSARY = CONFIG_DIR + '/nist_glossary_of_key_information_security_terms.cfg'
WORD_LIST = CONFIG_DIR + '/word_list.cfg'

ARXIV_DOMAIN = 'http://arxiv.org'
ARXIV_RECENT = ARXIV_DOMAIN + '/list/cs.CR/recent'


COMPUTER_HOPE = 'http://www.computerhope.com/jargon/j'
MANYTHINGS = 'http://www.manythings.org/vocabulary/lists/l/words.php?f=3esl.'


WORD_LEN_THRESHOLD = 25
INSTANCE_FILE_LIMIT = 1000
