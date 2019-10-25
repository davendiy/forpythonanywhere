#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 25.10.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

""" Generates the files with random text to the given
directory.
"""

import random
import time
from string import ascii_letters
import os
import logging

logging.basicConfig(level=logging.INFO)

CHUNK = 100 * 1024
DEFAULT_DIRECTORY = './ind_test_dir'
SIZE = 2 * 1024 * 1024
TIMEDELTA = 5
DEFAULT_FILENAME = 'test_file.txt'


def generate(filename, size):
    with open(filename, 'w', encoding='utf-8') as file:
        for _ in range(0, size, CHUNK):
            file.write(''.join(random.choice(ascii_letters)
                               for _ in range(CHUNK)))
        file.write(''.join(random.choice(ascii_letters)
                           for _ in range(size % CHUNK)))


def main(directory=DEFAULT_DIRECTORY, filename=DEFAULT_FILENAME,
         size=SIZE, sleep=TIMEDELTA):
    i = 0

    if not os.path.exists(directory):
        logging.info(f'[*] Creating a directory {directory}...')
        os.mkdir(directory)

    name, ext = os.path.splitext(filename)
    while True:
        tmp_name = f'{name}{i}{ext}'
        logging.info(f'[-->] Generating a file {tmp_name}...')
        generate(os.path.join(directory, tmp_name), size)
        logging.info(f'[*] Done. Sleep...')
        time.sleep(sleep)
        i += 1


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d', '--directory', type=str,
                        help=f'Testing directory. Default: {DEFAULT_DIRECTORY}')
    parser.add_argument('-t', '--time', type=float,
                        help='Time of being asleep.')
    parser.add_argument('-c', '--chunk', type=int,
                        help=f'Length of piece that is being written at once. Default: {CHUNK}')
    parser.add_argument('-f', '--filename', type=str,
                        help=f'Template of names of files. Default: {DEFAULT_FILENAME}')
    parser.add_argument('-s', '--size', type=int,
                        help=f'Size of files. Default: {SIZE}')
    args = parser.parse_args(sys.argv[1:])

    pars = {el: val for el, val in vars(args).items() if val is not None}
    if 'time' in pars:
        pars['sleep'] = pars['time']
        del pars['time']

    if 'chunk' in pars:
        CHUNK = pars['chunk']
        del pars['chunk']

    main(**pars)
