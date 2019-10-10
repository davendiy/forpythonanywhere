#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# created: 18.09.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


import os


def remove_copies(path):
    """Find all dublicates in the given path and
    delete all of them except the one that found higher.

    Parameters
    ----------
    path : string
        Absolute path of the directory.
    """
    # additional dictionary {(<name of file>, <size of file>): <absolute path>}
    # uses for finding dubplicates
    files = {}
    for dir_path, dir_names, file_names in os.walk(path):
        print(f"[*] Checking {dir_path}...")
        for filename in file_names:
            full_name = os.path.join(dir_path, filename)
            tmp_size = os.path.getsize(full_name)

            # check if we've already found the same file
            if (filename, tmp_size) in files:

                # delete file that has been found deeper
                if files[(filename, tmp_size)].count('/') > full_name.count('/'):
                    trash = files[(filename, tmp_size)]
                    files[(filename, tmp_size)] = full_name
                else:
                    trash = full_name

                print(f"[!!] Found dublicate: {filename}.\nRemoving {trash}...")
                os.remove(trash)
            else:
                files[(filename, tmp_size)] = full_name
    print("[*] Done.")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("Please, enter the path you want to clear: ")

    remove_copies(path)
