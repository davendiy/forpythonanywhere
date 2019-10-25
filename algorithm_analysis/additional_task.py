#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 13.10.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import numpy as np
from scipy.stats import bernoulli

rv = bernoulli(p=0.1)


def strange_algorithm(sequence: list):
    steps_amount = 0

    def _random_splitting(_sequence):
        list_of_pieces = []
        cur_piece = []
        for el in _sequence:
            if rv.rvs() and cur_piece:
                list_of_pieces.append(cur_piece)
                cur_piece = []
            cur_piece.append(el)
        if cur_piece:
            list_of_pieces.append(cur_piece)
        return list_of_pieces

    def _choose(_blocks):
        prev_chosen = False
        _chosen = []
        for _ in _blocks:
            tmp = rv.rvs()
            prev_chosen = bool(tmp) or not prev_chosen
            _chosen.append(prev_chosen)
        return _chosen

    def _reduction(_block):
        return list(filter(lambda x: x > 0, map(lambda y: y - 1, _block)))

    def _zip(_blocks, reducted):
        res = []
        for i, block in enumerate(_blocks):
            if reducted[i]:
                res += block
            else:
                res.append(block)
        return res

    def _unzip(_sequence):
        res = []
        for el in _sequence:
            if isinstance(el, list):
                res += el
            else:
                res.append(el)
        return res

    while sequence:
        steps_amount += 1
        blocks = _random_splitting(sequence)
        blocks = list(map(_unzip, blocks))
        chosen = _choose(blocks)
        blocks = list(map(lambda block, ischosen: _reduction(block) if ischosen else block, blocks, chosen))
        sequence = _zip(blocks, chosen)
        print(sequence)

    return steps_amount


d = 2
seq = list(np.random.randint(1, d, size=100000))

# print(list(map(lambda x, y: x + y, seq, seq)))

print(strange_algorithm(seq))
