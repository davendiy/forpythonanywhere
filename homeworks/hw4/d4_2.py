#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# created: 25.10.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

""" Simple eolymp-like tester of python programs.

Reads the tests from some text file, executes each of them in the another
subprocess and writes the result into the ouput file.

The tests must be in such format:
<path-to-python-file> (<comma-separated-args>) (<expected-type>: <expected-value>)

Example:
     ./d4_2_tests_program/test1.py (2, 96) (int: 98)
"""

import re
from subprocess import Popen, PIPE, TimeoutExpired
from concurrent.futures import ThreadPoolExecutor
from threading import RLock
import logging
import time
import os


lock = RLock()
logging.basicConfig(level=logging.DEBUG)

# translator of types
TYPES_DICT = {'int': int,
              'float': float,
              'str': str}

TIMEOUT = 2                     # max value of computation time
EPS = 1e-5                      # epsilon for float comparison
FILEOUT = "tests_result.txt"    # file for output
FILE_TESTS = "d4_2_tests.txt"   # source of tests

# regex for test
PATT = re.compile(r"""^(?P<directory>(?:(?:[^/ ]|(?:\\\ ))*/)*) # unix path like /home/user/Рабочий\ стол'
                      (?P<filename>(?:(?:[^/ ]|(?:\\\ ))+))   # the last non empty part of unix path
                      \s\(                       # (<comma-separated args>)
                      (?P<args>[A-Za-z,\s\d.]*)
                      \)\s
                      \(                         # (<type>: <value>)
                      (?P<res_type>[a-z_]*):\s?
                      (?P<res_value>[a-zA-Z\d\s.]+)
                      \)""", re.VERBOSE)


def test_function(program_path, args, expected_type, expected_value):
    """ Function that runs some python program with some arguments.
    Program execution is performed in the another subprocess.

    The given Python program must require some arguments from stdin, separated
    with \n in order to use simple input(). Result must be printed in
    stdout as the last line.

    Parameters
    ----------
    program_path       - absolute or relative path to the required program
    args               - a list of arguments
    expected_type      - type of expected data (int, float or str)
    expected_value     - value of expected data

    Returns
    -------
    (bool <succ>, str <status>, str <res_time>)
        succ      - True if the result is right and there was
                    no errors during execution
        status    - The result status of program execution
                    (Accepted, Wrong answer, etc)
        res_time  - The result execution time.
    """
    assert expected_type is int or expected_type is float or expected_type is str
    succ = False
    status = "Undefined."
    res_time = "0"

    # if the value is given as string, but with different type
    expected_value = expected_type(expected_value)

    params = ['python3', program_path]
    ps = Popen(params, stdin=PIPE, stderr=PIPE, stdout=PIPE)

    formatted_args = '\n'.join(args)  # \n-separated params
    try:
        t = time.time()       # computation time
        stdout, stderr = ps.communicate(input=bytes(formatted_args,
                                                    encoding='utf-8'),
                                        timeout=TIMEOUT)
        time.sleep(0)
        res_time = time.time() - t
        if stdout is None:            # there is output
            res_out = expected_type()
        else:
            res_out = expected_type(stdout.decode('utf-8'))
        if len(stderr):               # there was errors
            status = "Computation Error: " + stderr.decode('utf-8')
            succ = False
        else:
            with lock:    # compare the results
                if expected_type is str or expected_type is int:
                    succ = res_out == expected_value
                else:
                    succ = abs(expected_value - res_out) < EPS
                status = "Accepted." if succ else "Wrong answer."
    except TimeoutExpired:
            res_time = TIMEOUT
            status = "Time limit exceeded."
            succ = False
    except Exception as e:
        logging.error(e)
    return succ, status, res_time


def thread_func(fileout, program_path, args, expected_type, expected_value):
    """ Cover function for the one above. Uses in threads.
    Just runs the test_function, gets the results and writes them to the
    file, printing the information about the process.

    Parameters
    ----------
    fileout            - file for results
    program_path       - absolute or relative path to the required program
    args               - a list of arguments
    expected_type      - type of expected data (int, float or str)
    expected_value     - value of expected data
    """
    logging.debug(f'[*] Starting test for {program_path} with args: {args}...')
    succ, status, res_time = test_function(program_path, args, expected_type, expected_value)
    logging.debug(f'[!!] Tests for {program_path} with args {args} done!')

    output = f"""Test for {program_path} and {', '.join(args)}:
                 Successful - {succ}, Time - {res_time}, Status - {status}"""
    with lock:
        fileout.write(f'{"="*80}\n{output}\n{"="*80}\n\n')


def regex_handler(fileout, match):
    """ Auxiliary function for transforming the regex into parameters of
    functions above.

    Parameters
    ----------
    fileout     - file for writing the results
    match       - found regex
    """
    directory = match.group('directory')
    program = match.group('filename')
    args = match.group('args').split(', ')
    res_type = TYPES_DICT.get(match.group('res_type'), '')
    res_value = match.group('res_value')

    # must be all of them
    if not all([directory, program, args, res_value, res_type]):
        return

    filename = os.path.join(directory, program)

    # runs it in Pool
    executor.submit(thread_func, fileout, filename, args, res_type, res_value)


def tester(tests_file):
    """ Reads all the tests from file and runs each of them.

    Parameters
    ----------
    tests_file     - path to file with tests.
    """
    fileout = open(FILEOUT, 'w', encoding='utf-8')
    with open(tests_file, 'r', encoding='utf-8') as file:
        for line in file:
            tmp = PATT.match(line)
            if tmp:
                regex_handler(fileout, tmp)


if __name__ == '__main__':
    with ThreadPoolExecutor() as executor:
        tester(FILE_TESTS)
