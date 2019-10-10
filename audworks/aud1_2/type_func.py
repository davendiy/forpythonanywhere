#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 13.09.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import re

P_TYPE = re.compile(r"<type\s[\'\"](?P<type>[\w_]+)[\'\"]>")


def extract_type(some_object):
    return {k: P_TYPE.search(str(type(v))).group("type")
            for k, v in some_object.__cls__.__dict__.items()}
