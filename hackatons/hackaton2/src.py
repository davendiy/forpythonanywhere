#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 20.09.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import os

STATUSES = {'update', 'delete', 'create'}
EXTENSION = '.DS_Store'


class File:
    def __init__(self, timestamp=0.0, path_to_file='', status=''):
        self.timestamp = timestamp
        self.path_to_file = path_to_file
        self.status = status
        self._name = os.path.split(self.path_to_file)

    def __eq__(self, other):
        return self._name == other._name


def find_all_files(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if file != EXTENSION:
                to_append = File(os.path.getmtime(os.path.join(r, file)), os.path.join(r, file), 'sync')
                files.append(to_append)
    print(files)
    return files


def merge(prev_state, cur_state1, cur_state2):
    for file1 in cur_state1:
        for file2 in cur_state2:
            if file1 == file2:
                solve()


def solve(file1, file2):
    pass


if __name__ == '__main__':
    find_all_files('/Users/zoran/Desktop/Programming/Third_course/prog')
