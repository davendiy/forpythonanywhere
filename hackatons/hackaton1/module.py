#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 06.09.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import os
import re

RE = "[LETTERS]{AMOUNT}[_$#-+@&]{AMOUNT2}"

RE2 = r"[LETTERS_$#\-+@&]{AMOUNT}"


def create_re(word):
    tmp = RE.replace("LETTERS", word)
    res = RE.replace("LETTERS", word)
    res = res.replace("AMOUNT2", '0')
    res = res.replace("AMOUNT", str(len(word)))

    tmp2 = tmp.replace("AMOUNT2", '1')
    res = res + " | " + tmp2.replace("AMOUNT", str(len(word)-1))

    tmp3 = tmp.replace("AMOUNT2", '2')
    res = res + " | " + tmp3.replace("AMOUNT", str(len(word)-2))
    return res


def create_re2(word):
    res = RE2.replace("LETTERS", word)
    return res.replace("AMOUNT", str(len(word)))


trashed_path = os.path.realpath("words/trashed.txt")
words_path = os.path.realpath("words/words.txt")

with open(words_path) as file:
    words = file.read().split()

with open(trashed_path) as file:
    text = file.read()


for el in words:
    tmp_pattern = create_re2(el)
    text = re.sub(tmp_pattern, '', text)

print(text)
print(create_re2('test_word'))
