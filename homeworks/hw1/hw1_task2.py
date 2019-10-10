#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 12.09.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


import re


def create_pattern(words, ignore_cases=False,
                   only_whole_word=True, min_letters_amount=1):
    """Create pattern for list of words.

    Parameters
    ----------
    words : List(str)
        List of string - words we need to find.
    ignore_cases : bool
        True if it doesn't matter if word lowercase or uppercase.
    only_whole_word : bool
        True if we need to find only whole word 'example',
        not 'exam' or 'exampl'
    min_letters_amount : int
        Minimal amount of letters that could be recagnized as
        'part of the word'.

    Returns
    -------
    str
        Regex pattern.
    """

    if only_whole_word:
        patt = '|'.join(words)
    else:
        patt = ''
        for tmp in words:
            for i in range(len(tmp), min_letters_amount-1, -1):
                patt += '|' + tmp[:i]

        patt = patt.strip("|")
    if ignore_cases:
        res_patt = re.compile(patt, re.IGNORECASE)
    else:
        res_patt = re.compile(patt)

    return res_patt


if __name__ == '__main__':
    test_words = ['necessary', 'computer', 'anyone']
    print(create_pattern(test_words))
    print(create_pattern(test_words, ignore_cases=True))
    print(create_pattern(test_words, only_whole_word=False, min_letters_amount=3))
