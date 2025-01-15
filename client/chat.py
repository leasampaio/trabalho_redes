import threading
import socket

online = False

def print_messages(server_socket: socket.socket):
    global online

    while True:
        if not online:
            continue

        plaintext = server_socket.recv(1024).decode().strip()
        print(plaintext)

def get_input():
    global user_input
    while True:
        user_input = input()

user_input = ""

def chat(server_socket, keys):
    global online
    global user_input

    online = True

    output_thread = threading.Thread(target=print_messages, args=[server_socket])
    input_thread = threading.Thread(target=get_input)

    output_thread.start()
    input_thread.start()

    while True:
        message = user_input
        user_input = ""
        if not message or not message.strip():
            continue

        server_socket.send(message.encode())

        if message == "/quit":
            online = False
            break

    online = False