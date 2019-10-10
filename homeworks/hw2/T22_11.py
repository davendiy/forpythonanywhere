#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# created: 19.09.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

""" Archive directory and split the archive into peaces with allowable
size if necessary.

Usage: T22_11.py -p path -f format
path - absolute path to necessary dictionary
format - archive format: one of 'zip', 'tar', 'gztar', 'bztar', 'xztar'

-c --chunk=allowed_chunk       - change the value of allowed chunk
                                 in bytes (default - 100kB)
-h --help                      - show this help and exit

Examples:
    T22_11.py -p /home/doc/tmp -f tar -c 102400000
"""


import os
import shutil
import getopt
import sys


CHUNK = 102400


def usage():
    """ Print documentation.
    """
    print(__doc__)


def write_tom(filename, data):
    """Write some bytes data to filename.

    Parameters
    ----------
    filename : str
        Name of file.
    data : stream of bytes
        data need to be written
    """
    print(f"[>] Writing to {filename}...")
    with open(filename, 'wb') as file:
        file.write(data)


def archive(path, format):
    """Main function for archiving.

    Parameters
    ----------
    path : str
        Absolute path to directory.
    format : str
        Archive format. One of 'zip', 'tar', 'gztar', 'bztar', 'xztar'.
    """
    path = path.rstrip(os.sep)
    absolute_basename = path + '.' + format
    _, basename = os.path.split(path)

    print(f"[*] Making archive to {basename}.{format}...")
    shutil.make_archive(path, format, path)
    if os.path.getsize(absolute_basename) > CHUNK:

        tmp_path = path + f'_{format}_files'
        print(f"[!!] Exceeding the limit of size, splitting to {tmp_path}...")
        os.mkdir(tmp_path)
        i = 0
        with open(absolute_basename, 'rb') as file:
            while True:
                tmp_name = "{}_{:03}.{}".format(basename, i, format)
                abs_tmp_name = os.path.join(tmp_path, tmp_name)
                data = file.read(CHUNK)
                write_tom(abs_tmp_name, data)
                if len(data) < CHUNK:
                    break
                i += 1
        os.remove(absolute_basename)
        print(f"[*] Done.")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:f:c",
                                   ["help", "path", "format", "chunk"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        exit(0)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            exit(0)
        elif o in ('-p', '--path'):
            path = a
        elif o in ('-f', '--format'):
            format = a
        elif o in ('-c', '--chunk'):
            CHUNK = int(args[0])
        else:
            raise Exception("Unhandled option")
    archive(path, format)
