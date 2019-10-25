#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 25.10.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import socket


target_host = ''
target_port = 2001

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))

while True:
    data = input("--> ")
    client.send(bytes(data, encoding='utf-8'))
    if 'exit' in data:
        print("[*] Closing connection...")
        break
    resp = client.recv(4096)
    print(resp)
