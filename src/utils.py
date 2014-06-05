"""
Basic functional utilities.
"""

import re
import string as String
import os


def readLines(fileName):
    """
    Return list of lines from the file.
    """
    try:
        f = open(fileName, 'r')
        lines = [line for line in f]
        f.close()
        newlines = []
        for line in lines:
            line = line.strip()
            if (len(line) != 0):
                newlines.append(line)
        return newlines
    except:
        print 'File read error!'


def readString(fileName):
    """
    Read string from the file.
    """
    try:
        lines = readLines(fileName)
        return ' '.join(line for line in lines)
    except:
        if (lines is None):
            return ''


def writeString(fileName, string):
    """
    Write string to the file.
    """
    try:
        DIR = os.path.abspath(fileName + '/../')
        if not os.path.exists(DIR):
            os.makedirs(DIR)
        f = open(fileName, 'w')
        f.write(string)
        f.close()
    except Exception as e:
        print string
        print 'File write error! [' + str(e) + ']'
        exit()


def appendString(fileName, string):
    """
    Write string to the file.
    """
    try:
        DIR = os.path.abspath(fileName + '/../')
        if not os.path.exists(DIR):
            os.makedirs(DIR)
        f = open(fileName, 'a')
        f.write(string)
        f.close()
    except:
        print 'File write error!'


def filter_ascii(c):
    """
    Return ascii.
    """
    if (ord(c) < 32 or ord(c) > 126):
        return ''
    return c


def clean(string):
    """
    Cleans the string to have ascii characters.
    """
    if (string is None):
        return ''
    string = string.split()
    string = ' '.join(string)
    string = re.sub(r'&#\d+;', r' ', string)
    string = re.sub(r'&', r'and', string)
    string = string.encode('ascii',errors='ignore')
    new_string = ''
    for c in string:
        new_string = new_string + filter_ascii(c)
    return string
