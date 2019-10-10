#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 12.09.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import re
from collections import OrderedDict

PATT = r"\b[MDCLXVI]+\b"

DICTIONARY = OrderedDict({"CM": 900,
                          "CD": 400,
                          "XC": 90,
                          "XL": 40,
                          "IX": 9,
                          "IV": 4,
                          "M": 1000,
                          "D": 500,
                          "C": 100,
                          "L": 50,
                          "X": 10,
                          "V": 5,
                          "I": 1,
})


def rome2dec(string):
    tmp_string = string
    res = 0
    while tmp_string:
        for el in DICTIONARY:
            if tmp_string.startswith(el):
                res += DICTIONARY[el]
                tmp_string = tmp_string[len(el):]
                break
        else:
            raise ValueError(f"Unexpected letter in rome number: {tmp_string[0]}")
    return res


if __name__ == '__main__':
    years = []
    with open("hw1_task3_text.txt", "r", encoding="utf-8") as file:
        for line in file:
            years += [rome2dec(el) for el in re.findall(PATT, line)]

    for el in sorted(years):
        print(el)
