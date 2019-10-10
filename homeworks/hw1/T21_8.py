#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 12.09.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

"""Homework 1, individual task 1.

Variant 7.
"""

import re

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


if __name__ == '__main__':
    with open("T21_8_text.txt", "r", encoding="utf-8") as file:
        text = file.read()

    with open("T21_8_out.txt", "w", encoding="utf-8") as file:
        file.write(P_FLOAT_NUM.sub(sub_func, text))
