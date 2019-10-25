#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# created: 24.10.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import subprocess
from concurrent.futures import ThreadPoolExecutor
from threading import RLock
import os
import time
import sys
import re

import logging
logging.basicConfig(level=logging.INFO)

lock = RLock()

SOME_PATTERN = re.compile(r'some')
CHUNK = 100 * 1024
DEFAULT_DIRECTORY = './ind_test_dir'
SIZE = 2 * 1024 * 1024
TIMEDELTA = 5
DEFAULT_FILENAME = 'test_file.txt'

DIR_NICE = './dir_with_nice_files'
DIR_BAD = './dir_with_bad_files'

THREADS_AMOUNT = 5


CHECKED = set()


def check_file(filename):
    global CHECKED
    if filename in CHECKED:
        return None
    logging.info(f'[<--] Checking file {filename}...')
    succ = False
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read(CHUNK)
        while data:
            if SOME_PATTERN.search(data) is not None:
                succ = True
                break
            data = file.read(CHUNK)
    logging.info(f'[*] Done. File {filename} checked.')
    with lock:
        CHECKED.add(filename)
    return succ, filename


def move_file(file_from, file_to):
    logging.info(f'[-->] Moving {file_from} to {file_to}...')
    with open(file_from, 'rb') as infile:
        with open(file_to, 'wb') as outfile:
            data = infile.read(CHUNK)
            while data:
                outfile.write(data)
                time.sleep(0)
                data = infile.read(CHUNK)
    logging.info(f'[*] Done. File {file_from} moved. Removing it...')
    try:
        os.remove(file_from)
    except FileNotFoundError:
        pass


def future_hanler(future):
    res, filename = future.result()
    _, file = os.path.split(filename)
    if res is None:
        return
    if res:
        move_file(filename, os.path.join(DIR_NICE, file))
    else:
        move_file(filename, os.path.join(DIR_BAD, file))


params = f'python3 ind4_2_sub.py ' \
         f'-c {CHUNK} ' \
         f'-d {DEFAULT_DIRECTORY} ' \
         f'-s {SIZE} ' \
         f'-t {TIMEDELTA} ' \
         f'-f {DEFAULT_FILENAME}'.split()

try:
    os.mkdir(DIR_BAD)
    os.mkdir(DIR_NICE)
    os.mkdir(DEFAULT_DIRECTORY)
except FileExistsError:
    pass

prc = subprocess.Popen(params, stdout=sys.stdout, stderr=sys.stderr)

executor = ThreadPoolExecutor(max_workers=THREADS_AMOUNT)
try:
    while True:
        for file in os.listdir(DEFAULT_DIRECTORY):
            filename = os.path.join(DEFAULT_DIRECTORY, file)
            if os.path.isfile(filename) and file[0] != '.':

                tmp = executor.submit(check_file, filename)

                tmp.add_done_callback(future_hanler)
        time.sleep(12)
except Exception as e:
    print(e)
finally:
    prc.kill()
    executor.shutdown()
