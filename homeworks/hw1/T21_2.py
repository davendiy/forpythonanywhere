#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 12.09.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import re

# separator of sentences - symbol of end + space or \n + Start of next sentence
P_SEP = r"([\.?!\"]{1,4}[\s\n][A-ZА-ЯҐЄІЇ\"])|([\.?!\"]{1,4}\n)"
PATTERN = re.compile(P_SEP, re.DOTALL)


def get_coord(text):
    """Gets necessary coordinates for get_neccessary_parts.

    Returns only global position of each sentence in the text.

    Parameters
    ----------
    text : str
        Text where we're finding our pattern

    Returns
    -------
    list
        A list of tuples (<start>, <end>) where
        <start> - position of the first symbol of i-th  sentence
        <end> - position of the last symbol of i-th sentence
    """
    res = []
    pre_pos = 0
    for sep in PATTERN.finditer(text):
        res.append((pre_pos, sep.start()))
        pre_pos = sep.end() - 1
    return res


def get_coord2(file_stream):
    """Gets necessary coordinates for get_neccessary_parts.

    Returns global position of each sentence in the file and
    line number with position in line.

    Parameters
    ----------
    file_stream : _io.TextIOWrapper
        File object with text

    Returns
    -------
    (list, list)
        Returns 2 lists of tuples: [(<global start>, <global end>), ] and
                                   [(<line number>, <position in line>)],
        where:
            global start - position of the first symbol of i-th sentence in file
            global end - position of the last symbol of i-th sentence in file
            line number - number of line where found the start of i-th sentence
            position in line - position of the first symbol of i-th sentence in
                the <line number> line
    """
    res_ness_coord = []          # (<global start>, <global end>)
    res_task_coord = [(0, 0)]    # (<line number>, <position in line>)
    pre_pos = 0             # position of the end of previous separator
    line_num = 0            # obvious
    global_num = 0          # amount of letters before
    for line in file_stream:
        for sep in PATTERN.finditer(line):
            res_ness_coord.append((pre_pos, sep.start()+global_num))
            pre_pos = sep.end() - 1 + global_num
            res_task_coord.append((line_num, sep.end()-1))

        global_num += len(line)
        line_num += 1
    res_task_coord.pop()   # remove the end of last sentence
    return res_ness_coord, res_task_coord


def get_neccessary_parts(text, coord_list):
    """Get list of sentences by their coordinates of start/end.
    """
    return [text[tmp[0]:tmp[1]+1] for tmp in coord_list]


if __name__ == '__main__':
    with open("T21_2_text.txt", "r", encoding="utf-8") as file:
        test_text = file.read()
        file.seek(0)
        coord, task_coord = get_coord2(file)
        parts = get_neccessary_parts(test_text, coord)

    with open("t21_2_output.txt", "w", encoding="utf-8") as file:
        for num, el in zip(task_coord, parts):
            file.write(f"{str(num)}: {el.strip()}\n\n")
