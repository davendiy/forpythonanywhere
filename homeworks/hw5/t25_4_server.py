#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 25.10.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import socket
import re
from concurrent.futures import ThreadPoolExecutor
import logging


logging.basicConfig(level=logging.INFO)


def handle(client_socket: socket.socket):
    logging.info(f"[<--] Getting data from {client_socket}...")
    buffer = b'\n'
    client_socket.settimeout(2)
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            buffer += data
    except socket.timeout:
        pass
    
    logging.info(f"[*] Got data from {client_socket}!")
    regex, text = buffer.decode('utf-8').split("\n\n")

    regex = regex.strip()
    res = ''
    for el in re.finditer(regex, text):
        res += el.group() + "\n\n"

    logging.info(res)
    logging.info(f"[-->] Sending {res} to the {client_socket}...")
    client_socket.send(bytes(res, 'utf-8'))
    client_socket.close()
    logging.info(f'[*] {client_socket} successfully closed.')
    
    
host = ''
port = 2049

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

logging.info(f'[*] Listening on {host}:{port}')

with ThreadPoolExecutor() as executor:
    while True:
        client, addr = server.accept()
        logging.info(f'[*] Accepted connection from {addr[0]} {addr[1]}')
        executor.submit(handle, client)
        handle(client)
