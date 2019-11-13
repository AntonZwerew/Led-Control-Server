# -*- coding: utf-8 -*-

import socket
from time import sleep
from tkinter import *  # Чтобы не тащить Qt
import sys
import getopt

help_file_name = "README.md"
encoding = "utf-8"
server_addr = 'localhost'
get_command_args = "get-args"
server_port = 7777
use_gui = False
client = None
connected = False


try:
    options, args = getopt.getopt(sys.argv[1:], 'hs:p:g', ['help', 'serv=', 'port=', 'gui'])
except getopt.GetoptError:
    print("Unknown options, try -h")
    sys.exit(2)

for opt, value in options:
    if opt in ('-h', '--help'):
        with open(help_file_name, "r", encoding=encoding) as help_file:
            help_msg = help_file.read()
            print(help_msg)
        sys.exit(0)
    elif opt in ('-s', '--serv'):
        server_addr = value
        print(f"Server address: {value}")
    elif opt in ('-p', '--port'):
        server_port = int(value)
        print(f"Server port {value}")
    elif opt in ('-g', '--gui'):
        use_gui = True

address_to_server = (server_addr, server_port)

client = None
connected = False


def create_interface():

    root = Tk()
    root.geometry("200x400")
    root.resizable(False, True)
    command_buttons_frame = Frame(root)
    log_frame = Frame(root)
    args_entry = Entry(root)

    log = Label(log_frame, wraplength=200)
    log_frame.pack()
    log.pack()
    args_entry.pack()
    exit_button = Button(root, text="EXIT")
    command_buttons = []

    def run_button_command(event):
        command = event.widget['text']
        if args_entry.get():
            command += " " + args_entry.get()
        result = run_request(command)  # widget - на чем произошел ивент
        result = str(result, encoding=encoding)
        log["text"] = ""
        if "OK" in result:
            args_entry.delete(first=0, last=END)
        log["text"] += result
        return result

    def exit_gui(event):
        sys.exit(0)

    for command in get_available_commands():
        command_buttons.append(Button(command_buttons_frame, text=command))

    for button in command_buttons:
        button.bind("<Button-1>", run_button_command)
        button.pack()

    exit_button.bind("<Button-1>", exit_gui)
    command_buttons_frame.pack()
    exit_button.pack()
    root.mainloop()


def get_available_commands():
    result = str(run_request("get-commands"), encoding=encoding)
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
            print(f"request: {str(request, encoding=encoding)}")
            return run_request(request)
    ans = client.recv(1024)  # TODO Если ответ больше
    return ans


ensure_connection()
if use_gui:
    create_interface()
    sys.exit(0)

while True:
    request = input("request:")
    try:
        client.send(bytes(request + "\n", encoding=encoding))
        ans = client.recv(1024)
        print(f"response: {str(ans, encoding=encoding)}")
    except ConnectionResetError or ConnectionRefusedError:
        ensure_connection()
        if request != "":
            client.send(bytes(request + "\n", encoding=encoding))
            ans = client.recv(1024)
            print(f"request: {request}")
            print(f"response: {str(ans, encoding=encoding)}")

