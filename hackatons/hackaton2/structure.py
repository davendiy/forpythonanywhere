#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import os
import time

UPDATED = 0
DELETED = 1
CREATED = 2
NICE = 3


class File:

    def __init__(self, root='', relative_path='', timestamp=0, status=NICE):
        self._relative_path = relative_path
        self._timestamp = timestamp
        self._root = root
        self._status = status

    @property
    def relative_path(self):
        return self._relative_path

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def root(self):
        return self._root

    @property
    def status(self):
        return self._status

    def __hash__(self):
        return hash(self.relative_path)

    def __eq__(self, other):
        return self.relative_path == other.relative_path


class Stamp:

    def __init__(self):
        self._dict = {}

    def symmetric_difference(self, other):
        return set(self._dict.keys()).symmetric_difference(other.keys())

    def intersection(self, other):
        return set(self._dict.keys()).intersection(other._dict.keys())

    def union(self, other):
        return set(self._dict.keys()).union(other._dict.keys())

    def difference(self, other):
        return set(self._dict.keys()).union(other._dict.keys())

    def add(self, file: File):
        self._dict[file.relative_path] = file

    def remove(self, file: File):
        self._dict.pop(file.relative_path)


class Synchronizer:

    def __init__(self, directory1, directory2):
        self._dir1 = directory1
        self._dir2 = directory2
        self._stamp = Stamp()
        self.synchronize()

    @property
    def directories(self)->tuple:
        """
        :return: (<dir1>, <dir2>)
        """
        return self._dir1, self._dir2

    @property
    def cur_stamp(self) -> Stamp:
        """"""
        return self._stamp

    def synchronize(self):
        stamp1 = self._scan(self._dir1)
        stamp2 = self._scan(self._dir2)
        res_stamp = self._merge(stamp1, stamp2)
        # will implicitly update self._stamp
        self._save_changes(res_stamp)

    def _scan(self, directory)->Stamp:
        """ Просканувати папочку і знайти файли/папки, які змінились

        :param directory: абсолютний путь до папки
        :return: Stamp(<files>)
        """
        next_stamp = Stamp()                 # TODO
        for root, dirs, files in os.walk(directory):
            for file in files:
                rel_path = os.path.join(root, file)
                tmp_file = File(directory, )

    def _merge(self, stamp1, stamp2)->Stamp:       # TODO
        ...

    def _solve_conflict(self, file1, file2) -> File:
        tmp = None
        if file1.status() == file2.status == CREATED or file1.status == file2.status == UPDATED:
            if file1.timestamp > file2.timestamp:
                tmp = File(file1.root, file1.relative_path, file1.timestamp, CREATED)
            else:
                tmp = File(file2.root, file2.relative_path, file2.timestamp, CREATED)
        elif file1.status == UPDATED and file2.status == DELETED:
            tmp = File(file2.root(), file2.relative_path, file2.timestamp, CREATED)
        elif file2.status == UPDATED and file1.status == DELETED:
            tmp = File(file1.root(), file1.relative_path, file1.timestamp, CREATED)
        return tmp

    def _save_changes(self, new_stamp):       # TODO
        ...

    def _save_file(self, file):               # TODO
        ...

    def _delete_file(self, file):             # TODO
        ...

    def _create_file(self, file):             # TODO
        ...


class Scheduler:

    def __init__(self, dir1, dir2):
        self._synchronizer = Synchronizer(dir1, dir2)

    def mainloop(self, polling_delay=10):
        while True:
            self._synchronizer.synchronize()
            time.sleep(polling_delay)