# -*- coding: utf-8 -*-

import socket
from time import sleep
from tkinter import *  # Чтобы не тащить Qt

encoding = "utf-8"  # важно, иначе не пройдет сравнение на сервере
address_to_server = ('localhost', 7777)

client = None
connected = False


def create_interface():
    root = Tk()
    command_buttons_frame = Frame(root)
    log_frame = Frame(root)

    log = Label(log_frame)
    log.pack()
    log_frame.pack()

    command_buttons = []
    for command in get_available_commands():
        command_buttons.append(Button(command_buttons_frame, text=command))
    for button in command_buttons:
        button.bind("<Button-1>", run_button_command)
        button.pack()

    command_buttons_frame.pack()
    root.mainloop()


def run_button_command(event):
    global log
    result = run_request(event.widget['text'])  # widget - на чем произошел ивент
    log["text"] += result
    return result


def get_available_commands():
    result = run_request("show-commands")
    result = result.decode(encoding)
    if result.startswith("OK ") and result.endswith("\n"):
        result = result[3:]  # убираем "OK "
        result = result[:-1]  # убираем "\n"
    else:
        # ответ некорректный
        return
    return result.split(", ")


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


def run_request(request):
    try:
        client.send(bytes(request + "\n", encoding=encoding))
    except ConnectionRefusedError or ConnectionResetError:
        ensure_connection()
        if request != "":
            print(f"request: {request}")
            return run_request(request)
    ans = client.recv(1024)  # TODO Если ответ больше
    return ans


ensure_connection()
# create_interface()

# TODO если успел сервер и были посланы данные - пересылать из после поднятиея сервера
while True:
    request = input("request:")
    print(f"response: {run_request(request)}")

