# -*- coding: utf-8 -*-

import socket
from time import sleep

encoding = "utf-8"  # важно, иначе не пройдет сравнение на сервере
address_to_server = ('localhost', 7777)

client = None
connected = False


def ensure_connection():
    global connected
    global client
    if connected:
        client.close()
        del client
        print(f"Server aborted connection, reconnecting ...")
        connected = False
    while not connected:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(address_to_server)
            connected = True
        except ConnectionRefusedError or OSError:
            print("Remote server refuses connection, reconnecting ...")
            sleep(2)


ensure_connection()

# TODO если успел сервер и были посланы данные - пересылать из после поднятиея сервера
while True:
    request = input("request:")
    try:
        client.send(bytes(request + "\n", encoding=encoding))
        ans = client.recv(1024)
        print(f"response: {ans}")
    except ConnectionResetError or ConnectionRefusedError:
        ensure_connection()
        if request != "":
            client.send(bytes(request + "\n", encoding=encoding))
            ans = client.recv(1024)
            print(f"request: {request}")
            print(f"response: {ans}")

