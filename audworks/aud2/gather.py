#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from collections import defaultdict


def get_info(absolute_dir):
    res = defaultdict(set)
    for root, dirs, files in os.walk(absolute_dir):
        for file in files:
            tmp_name, tmp_ext = os.path.splitext(file)
            res[tmp_ext].add(os.path.join(root, file))
    return res


if __name__ == '__main__':
    path = input('absolute path to dir: ')
    print('[*] Collecting information...')
    tmp = get_info(path)
    print('[*] Saving to files')
    if not os.path.exists('info'):
        os.mkdir('info')
    for ext in tmp:
        with open(f"info/{ext.strip('.')}.txt", 'w') as file:
            for el in tmp[ext]:
                file.write(el+'\n')
    
