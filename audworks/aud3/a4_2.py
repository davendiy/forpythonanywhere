#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 11.10.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import tkinter as tk
from tkinter import ttk
import threading
from tkinter.messagebox import showinfo

lock = threading.RLock()

FIB = {}


def fib(n):
    if n < 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def handle_fib(n):
    res = fib(n)
    showinfo('Result', f'fib{n} = {res}')


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        _entry = ttk.Entry(self)
        _entry.pack(side=tk.TOP)
        self._n = tk.StringVar()
        ttk.Button(self, text="Calculate", command=self._calc_handler)

    def _calc_handler(self, ev=None):
        if self._entry:
            pass
        threading.Thread(target=handle_fib, args=())
