#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# created: 19.09.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


import os

OUTPUT_FILENAME = "T22_1.out"


def get_diffs(path1, path2):
    """Find the differences between directories path1 and path2.
    Checks only files in the first level of directories.

    Parameters
    ----------
    path1 : str
        Absolute path to the first directory
    path2 : str
        Absolute path to the second directory

    """
    print(f"[*] Checking for differences between {path1} and {path2}...")
    first_files = {name for name in os.listdir(path1)
                   if os.path.isfile(os.path.join(path1, name))}
    second_files = {name for name in os.listdir(path2)
                    if os.path.isfile(os.path.join(path2, name))}
    res = first_files.symmetric_difference(second_files)
    for name in res:
        print(f"[!!] Found difference: {name}")
    print("[*] Done.")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 2:
        path1, path2 = sys.argv[1], sys.argv[2]
    else:
        path1 = input("please, enter the path of the first dictionary: ")
        path2 = input("please, enter the path of the second dictionary: ")

    prev = sys.stdout
    sys.stdout = open(OUTPUT_FILENAME, 'w')

    get_diffs(path1, path2)
    sys.stdout.close()
    sys.stdout = prev
