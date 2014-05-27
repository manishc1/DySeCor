"""
Basic functional utilities.
"""

import re
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
            if (len(line.strip()) != 0):
                newlines.append(line)
        return newlines
    except:
        print 'File read error!'


def readString(fileName):
    """
    Read string from the file.
    """
    lines = readLines(fileName)
    return ' '.join(line for line in lines)


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
    except:
        print 'File write error!'

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


def clean(string):
    """
    Cleans the string to have ascii characters.
    """
    string = string.split()
    string = ' '.join(string)
    string = re.sub(r'&#\d+;', r' ', string)
    string = re.sub(r'&', r'and', string)
    return string
