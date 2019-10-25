#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 25.10.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import socket

host = ''
port = 2048

regex = r"\(Варіант \d\)"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
print(f'[*] Connected to {host}, {port}.')

client.send(bytes(regex + '\n\n', encoding='utf-8'))

print(f'[-->] Sent {regex}...')

with open("t25_4_text.txt", 'rb') as file:
    while True:
        data = file.read(4096)
        if not data:
            break
        print(f'[-->] Sending data...')
        client.send(data)

response = b' '
print("[<--] Receiving...")
while True:
    tmp = client.recv(4096)
    if not tmp:
        break
    response += tmp

print("[*] Got it!")
print(response.decode('utf-8'))
