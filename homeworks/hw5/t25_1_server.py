#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 25.10.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import socket
from concurrent.futures import ThreadPoolExecutor
import logging
import datetime


logging.basicConfig(level=logging.INFO)

def getdate(datestr):
    if '.' in datestr:
        dateformat = "%d.%m.%Y"
    elif '-' in datestr:
        dateformat = "%Y-%m-%d"
    else:                                   # if '/' in datestr:
        dateformat = "%m/%d/%Y"
    return str(datetime.datetime.strptime(datestr,dateformat))


def handle(client_socket: socket.socket):
    try:
        logging.info(f"[<--] Getting data from {client_socket}...")

        data = client_socket.recv(4096).decode('utf-8').strip()
        logging.info(f"[*] Got data from {client_socket}!")

        res = getdate(data)

        logging.info(res)
        logging.info(f"[-->] Sending {res} to the {client_socket}...")
        client_socket.send(bytes(res, 'utf-8'))
        client_socket.close()
        logging.info(f'[*] {client_socket} successfully closed.')
    except Exception as e:
        logging.error(e)


host = ''
port = 2041

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

logging.info(f'[*] Listening on {host}:{port}')

with ThreadPoolExecutor() as executor:
    while True:
        client, addr = server.accept()
        logging.info(f'[*] Accepted connection from {addr[0]} {addr[1]}')
        executor.submit(handle, client)
        # handle(client)
