#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 11.10.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import threading
import time
import datetime


def clock():
    while True:
        print(datetime.datetime.now())
        time.sleep(1)


thread = threading.Thread(target=clock())
thread.start()
thread.join()
