import threading
import socket

online = False

def handle_messages(server_socket: socket.socket):
    global online

    if not online:
        return

    plaintext = server_socket.recv(1024).decode().strip()
    print(plaintext)

def chat(server_socket, keys):
    global online
    online = True

    while True:
        threading.Thread(target=handle_messages, args=[server_socket]).start()

        message = input("> ")
        if not message.strip():
            continue

        if message == "/quit":
            online = False
            break

        server_socket.send(message.encode())

    online = False