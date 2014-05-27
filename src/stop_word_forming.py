#! /usr/bin/python


from constants import *
from utils import *


STOP_WORD_FILE_OLD = CONFIG_DIR + '/stop_words_old.cfg'
STOP_WORD_FILE_NEW = CONFIG_DIR + '/stop_words_new.cfg'


def main():
    lines = readLines(STOP_WORD_FILE_OLD)
    stop_words = []
    for line in lines:
        words = line.strip().lower().split()
        stop_words = stop_words + words
    stop_words = list(sorted(set(stop_words)))
    writeString(STOP_WORD_FILE_NEW, '\n'.join(stop_words))


if __name__ == "__main__":
    main()
