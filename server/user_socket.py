from memory_data import *
from user_actions import *

import socket
import threading
import traceback 
import logging

def handle_client(client_socket: socket.socket, client_address):
    try:
        handle_client_unsafely(client_socket, client_address)
    except Exception as e:
        logging.error(f"Erro: {e}")
        traceback.print_exc() 
    finally:
        client_socket.close()

def handle_client_unsafely(client_socket: socket.socket, client_address):
    logging.info(f"Conexão {client_address} estabelecida.")

    def waitFor(input_name):
        client_socket.send(f"GET {input_name}".encode())
        value = client_socket.recv(1024).decode().strip()
        return value

    def send(message):
        client_socket.send(message.encode())
        
    def endMessage():
        client_socket.send("END_OF_MESSAGE".encode())

    while True:
        raw_message = client_socket.recv(1024).decode().strip()

        option = raw_message.split(" ")[0].upper()
        args = raw_message.split(" ")[1:]
        
        logging.info(f"Mensagem \"{raw_message}\" recebida de {client_address}.")

        match option:
            case "QUIT":
                break
            case "REGISTER":
                if len(args) < 2:
                    send("1")
                    send("Digite seu usuário e senha")
                    endMessage()
                    continue

                user_name = args[0]
                user_password = args[1]
                
                if len(args) > 2:
                    send("1")
                    send("Seu nome e senha não podem conter espaços!")
                    endMessage()
                elif user_name in users:
                    send("1")
                    send("Usuário já cadastrado")
                    endMessage()
                else:
                    send("0")
                    endMessage()
                    create_user(user_name, user_password, client_socket)
                    logging.info(f"Usuário {user_name} cadastrado.")
            case "LOGIN":
                if len(args) < 2:
                    send("1")
                    send("Digite seu usuário e senha")
                    endMessage()
                    continue

                user_name = args[0]
                user_password = args[1]

                public_key = waitFor("public_key")

                if (user_name in users and users[user_name]["password"] == user_password):
                    user = users[user_name]
                    user["public_key"] = public_key
                    user["client_socket"] = client_socket

                    send("0")
                    send("Usuário autenticado")
                    endMessage()

                    join_room(user, MAIN_ROOM)
                    chat(user)
                else:
                    send("1")
                    send("Usuário ou senha inválidos")
                    endMessage()
            case "":
                break
            case _:
                continue