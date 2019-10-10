#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danil Kovalenko


import os

STATUSES = {'update', 'delete', 'create'}


class File:
    def __init__(self, timestamp=0.0, path_to_file='', status='', root=''):
        self.timestamp = timestamp
        self.path_to_file = path_to_file    # relative path
        self.status = status
        self.root = root                     # path to directory

    def copy(self):
        return File(timestamp=self.timestamp, path_to_file=self.path_to_file, status=self.status, root=self.root)


def find_all_files(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if file != '.DS_Store':
                to_append = File(os.path.getmtime(os.path.join(r, file)),
                                 os.path.join(r, file),
                                 'sync')
                files.append(to_append)
    print(files)
    return files


class Change:
    """Data about new coming changes"""

    def apply_change_locally(self, full_path_to_dir):
        """change data on disk"""

    def append(self, file):
        pass

class Stamp:
    """Data about all last files"""

    def modify_according_to_change(self, c: Change):
        pass

    def __contains__(self, item):
        pass

    def __iter__(self):
        pass

class DirTree:

    def __init__(self):
        self._old_stamp = None   # type: Stamp

    def _make_init_stamp(self):
        """make first stamp of directory. All files marked as created"""

    def scan(self, abs_path) -> Change:
        """Retrieve Change for cur dir"""
        res_change = Change()
        files = find_all_files(abs_path)
        for file1 in self._old_stamp:    # type: File
            found = False
            for file2 in files:          # type: File
                if file1 == file2:
                    found = True
                    if file1.timestamp != file2.timestamp:
                        res_file = file2.copy()
                        res_file.status = 'update'
                        res_file.root = abs_path
                        res_change.append(res_file)
                    break
            if not found:
                res_file = file1.copy()   # type: File
                res_file.status = 'delete'
                res_file.root = abs_path
                res_change.append(res_file)
        for file1 in files:
            found = False
            for file2 in self._old_stamp:
                if file1 == file2:
                    found = True
                    break
            if not found:
                res_file = file1.copy()
                res_file.status = 'create'
                res_file.root = abs_path
                res_change.append(res_file)
        return res_change

    def resolve_conflict(self, change1, change2):
        """Scans two changes for conflits, return one with solved conflicts"""
        pass

    def _solve_conflict(self, file1, file2):
        pass

    def apply_change_to_stamp(self, change):
        """merge stamp and change"""
        pass


class Sync:

    def do_sync(self, dir_path, c: Change):
        c.apply_change_locally(dir_path)