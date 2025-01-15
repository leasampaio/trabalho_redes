from config_vars import *
from crypto_methods import *

import threading
import socket

keys = generate_keys()
server_key = None
online = False
user_input = ""

def start(server_socket):
    keys = generate_keys()
    online = False
    server_key = None
    server_socket.connect((HOST, PORT))

    print()
    print("Conexão com o servidor estabelecida!")
    print()

    def get_messages():
        messages = []
        while True:
            encrypted = server_socket.recv(1024)
            message = decrypt(keys["private"], encrypted)
            if message != "END_OF_MESSAGE":
                messages.append(message)
            else:
                return messages
  
    while True:
        if not server_key:
            server_key = server_socket.recv(1024)
            server_socket.send(keys["public"])
            continue

        print("Escolha uma opção:")
        print("[0] Sair")
        print("[1] Registrar")
        print("[2] Login")

        message = input("> ")

        def send(message):
            encrypted = encrypt(server_key, message)
            server_socket.send(encrypted)

        match message:
            case "0":
                server_socket.close()
                exit(0)
                break

            case "1":
                print("\n")
                user_name = input("Usuário: ")
                user_password = input("Senha: ")

                send(f"REGISTER {user_name} {user_password}")

                response = get_messages()

                if response[0] == "0":
                    print("\nUsuário cadastrado com sucesso\n")
                else:
                    print(f"\nErro: {response[1]}\n")

            case "2":
                print("\n")

                user_name = input("Usuário: ")
                user_password = input("Senha: ")

                send(f"LOGIN {user_name} {user_password}")

                response = get_messages()

                if response[0] == "0":
                    print("\nUsuário autenticado\n")
                    chat(server_socket, server_key, keys)
                else:
                    print(f"\nErro: {response[1]}\n")

def print_messages(server_socket: socket.socket, keys):
    global online
    while online:
        try:
            encrypted = server_socket.recv(1024)
            message = decrypt(keys["private"], encrypted)
            print(message)
        except Exception as e:
            server_socket.close()
            online = False
            break

def get_input():
    global user_input
    global online
    while online:
        user_input = input()

def chat(server_socket, server_key, keys):
    global online
    global user_input

    print("Conectado ao chat!")
    print("Digite /quit para sair do chat")
    print("Digite /w <usuário> <mensagem> para enviar uma mensagem privada")
    print("Digite /r <mensagem> para responder à última mensagem privada recebida")
    print("Digite /join <sala> para entrar numa sala")
    print("Digite /leave para sair de uma sala e voltar à sala geral")

    online = True

    output_thread = threading.Thread(target=print_messages, args=[server_socket, keys])
    input_thread = threading.Thread(target=get_input)

    output_thread.start()
    input_thread.start()

    while True:
        if not online:
            raise Exception("Conexão com o servidor perdida!")
            break
            
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