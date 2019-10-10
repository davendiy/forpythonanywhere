#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from docx import Document
import re
import os

P_FLOAT_NUM = r"""([\s\n]|^)      # space, \n or the begining of line
                  (?P<sign>[+-]?)           # sign
                  ((?P<before1>\d+)?\.(?P<after1>\d+)  # 123123.123123 or .1231
                  |(?P<before2>\d+)\.(?P<after2>\d+)?) # 124124.12312 or 123213.
                  ([\s\n]|$)      # space, \n or the end of line
               """
P_FLOAT_NUM = re.compile(P_FLOAT_NUM, re.VERBOSE)


def sub_func(match):
    before, after = match.group("before1"), match.group("after1")
    sign = match.group("sign")
    if not before and not after:
        before, after = match.group("before2"), match.group("after2")
    before = before if before else "0"
    after = after if after else "0"
    # print(f"{sign}{before}.{after}")
    return f"{sign}{before}.{after} "


def doc_handler(filename):
    doc = Document(filename)
    for par in doc.paragraphs:
        par.text = P_FLOAT_NUM.sub(sub_func, par.text)
    name, ext = os.path.splitext(filename)
    new_filename = name + '_changed' + ext
    doc.save(new_filename)


if __name__ == '__main__':
    doc_handler('test.docx')
