#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 25.10.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import socket
from concurrent.futures import ThreadPoolExecutor
from threading import RLock
import re
import logging

logging.basicConfig(level=logging.INFO)

VAR_PATT = re.compile(r"[a-zA-Z_][a-zA-Z_\d]*")
lock = RLock()


def handler(client, addr):
    logging.info(f"[*] Connected to {addr}.")
    glob = {}
    while True:
        # logging.info(glob)
        logging.info(f"[<--] Getting data from {addr}...")
        codeline = client.recv(4096).decode(encoding='utf-8')
        logging.info(codeline)
        if 'exit' in codeline:
            client.close()
            logging.info("[*] Closing connection..")
            break
        var, exp = codeline.split("=")

        if not VAR_PATT.match(var):
            client.send(b"SyntaxError")
            continue
        try:
            with lock:
                tmp = eval(exp, glob)
                glob[var.strip()] = tmp
                logging.info(f"[-->] Sending data to {addr}...")
            client.send(bytes(str(tmp), encoding='utf-8'))
        except Exception as e:
            logging.info(f"[-->] Sending data to {addr}...")
            client.send(bytes(str(e), encoding='utf-8'))


server_host = ''
server_port = 2001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_host, server_port))
server.listen(5)

with ThreadPoolExecutor() as executor:
    while True:
        client, addr = server.accept()
        logging.info(f'[*] Accepted connection from {addr[0]} {addr[1]}')
        executor.submit(handler, client, addr)
        # handler(client, addr)
