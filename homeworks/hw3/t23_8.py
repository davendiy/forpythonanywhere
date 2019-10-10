#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 10.10.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

""" This program helps you to find and replace all the regex patterns
in all the Word-files in some directory.


"""

import re
import docx
import os
import getopt
import sys
import datetime


POSSIBLE_EXTENSIONS = {".doc", ".docx", ".wbk", ".docm", ".dotx"}


def usage():
    print(__doc__)


def _find_replace(regex, sub, filename):
    doc = docx.Document(filename)
    for par in doc.paragraphs:
            par.text = regex.sub(sub, par.text)
    doc.save(filename)


def find_replace(regex, sub, path):
    for root, dirs, files in os.walk(path):
        print(f"[*] Checking {root}...")
        for file in files:
            name, ext = os.path.splitext(file)
            if ext in POSSIBLE_EXTENSIONS:
                tmp_path = os.path.join(root, file)
                try:
                    _find_replace(regex, sub, tmp_path)
                except Exception as e:
                    print(f"[!] Exception in {tmp_path}: {e}. Skipping...")


def getdate(datestr):
    """Повертає дату як об'єкт за рядком дати datestr у різних форматах.

    Можливі формати дати:
    dd.mm.yyyy
    yyyy-mm-dd
    mm/dd/yyyy
    """
    if '.' in datestr:
        dateformat = "%d.%m.%Y"
    elif '-' in datestr:
        dateformat = "%Y-%m-%d"
    else:                                   # if '/' in datestr:
        dateformat = "%m/%d/%Y"
    return datetime.datetime.strptime(datestr,dateformat)


def test():
    # regex for date
    test_re = r'''(\d{1,2}\.\d{1,2}\.\d{4}   
                  |\d{4}-\d{1,2}-\d{1,2}     
                  |\d{1,2}/\d{1,2}/\d{4})    
               '''
    test_re = re.compile(test_re)

    test_path = "./t23_8_test_dir"

    def test_sub(re_match):
        word = re_match.group()
        return getdate(word).strftime("%b %d %Y")

    find_replace(test_re, test_sub, test_path)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        test()
        exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:r:s",
                                   ["help", "path", "format", "chunk"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        exit(0)
