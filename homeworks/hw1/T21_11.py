#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 12.09.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

"""Homework 1, individual task 2.

Variant 1.
"""

import re
import random


P_WORD = re.compile(r"\b[A-ZА-ЯЁЪ]+\b", re.IGNORECASE)
CHANGES_FREQUENCY = 0.5

POSSIBLE_CHANGES = {"в": "фф",
                    "а": "о",
                    "о": "а",
                    "и": "ы",
                    "я": "йа",
                    "е": "и",
                    "к": "г",
                    "п": "б",
                    "х": "г",
                    "ш": "ж",
                    "ж": "ш",
                    "з": "с",
                    "ь": ""}

tmp = {}
for k, v in POSSIBLE_CHANGES.items():
    tmp[k.upper()] = v.upper()

POSSIBLE_CHANGES.update(tmp)


def change_word(match):
    word = match.group()
    res_word = word

    if random.randint(1, 10) > CHANGES_FREQUENCY * 10:
        return res_word

    for i in range(random.randint(1, 2)):
        chunk = len(word) * 5
        count = 0
        ind = random.randint(0, len(word)-1)
        while word[ind] not in POSSIBLE_CHANGES and count < chunk:
            ind = random.randint(0, len(word)-1)
            count += 1
        if word[ind] in POSSIBLE_CHANGES:
            res_word = res_word[:ind] + POSSIBLE_CHANGES[word[ind]] + res_word[ind+1:]
    return res_word


if __name__ == '__main__':
    with open('T21_11_text.txt', 'r', encoding="utf-8") as file:
        text = file.read()

    res_text = P_WORD.sub(change_word, text)
    with open("T21_11_out.txt", 'w', encoding='utf-8') as file:
        file.write(res_text)
