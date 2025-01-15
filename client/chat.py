from crypto_methods import *

import threading
import socket

online = False

def print_messages(server_socket: socket.socket, keys):
    global online

    while True:
        if not online:
            continue

        encrypted = server_socket.recv(1024)
        message = decrypt(keys["private"], encrypted)
        print(message)

def get_input():
    global user_input
    while True:
        user_input = input()

user_input = ""

def chat(server_socket, server_key, keys):
    global online
    global user_input

    online = True

    output_thread = threading.Thread(target=print_messages, args=[server_socket, keys])
    input_thread = threading.Thread(target=get_input)

    output_thread.start()
    input_thread.start()

    while True:
        message = user_input
        user_input = ""
        if not message or not message.strip():
            continue

        encrypted = encrypt(server_key, message.strip())
        server_socket.send(encrypted)

        if message == "/quit":
            online = False
            break

    online = False