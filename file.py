import socket
from pathlib import Path

def client_file_send(server_socket: socket.socket):
    path = input("Nome do arquivo: ")
    path = Path(path)

    if not path.is_file():
        raise Exception(f"Arquivo '{path}' inválido.")

    with open(path, "rb") as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            server_socket.sendall(data)
    
    print("Arquivo enviado.")


def server_file(client_socket_from: socket.socket, client_socket_to: socket.socket):
    while True:
        data = client_socket_from.recv(1024)
        if not data:
            break
        client_socket_to.sendall(data)


def client_file_receive(server_socket: socket.socket):
    filename = "file"
    path = Path(filename)
    i = 1
    while path.is_file():
        path = Path(f"{filename}-{i}")
        i += 1

    with open(path, "wb") as f:
        while True:
            data = server_socket.recv(1024)
            if not data:
                break
            f.write(data)
