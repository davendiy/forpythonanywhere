#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 25.10.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import socket

host = ''
port = 2041

data = input("Please, enter the date: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
print(f'[*] Connected to {host}, {port}.')

client.send(bytes(data + '\n\n', encoding='utf-8'))

print(f'[-->] Sent {data}...')

response = client.recv(4096)
print("[<--] Receiving...")

print("[*] Got it!")
print(response.decode('utf-8'))
