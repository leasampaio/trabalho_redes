from config_vars import *
from crypto_methods import *
from chat import *

import threading

def start(server_socket):

    server_socket.connect((HOST, PORT))

    print()
    print("Conexão com o servidor estabelecida!")
    print()

    def get_messages():
        messages = []
        while True:
            message = server_socket.recv(1024).decode().strip()
            if message != "END_OF_MESSAGE":
                messages.append(message)
            else:
                return messages

    def send_input(key, value, no_encode=""):
        message = server_socket.recv(1024).decode().strip()
        if message.startswith("GET") and message.endswith(key):
            server_socket.send(value if no_encode else value.encode())
  
    while True:
        print("Escolha uma opção:")
        print("[0] Sair")
        print("[1] Registrar")
        print("[2] Login")

        message = input("> ")

        match message:
            case "0":
                server_socket.send("QUIT".encode())
                break

            case "1":
                print("\n")
                user_name = input("Usuário: ")
                user_password = input("Senha: ")

                server_socket.send(f"REGISTER {user_name} {user_password}".encode())

                response = get_messages()

                if response[0] == "0":
                    print("\nUsuário cadastrado com sucesso\n")
                else:
                    print(f"\nErro: {response[1]}\n")

            case "2":
                print("\n")
                keys = generate_keys()

                user_name = input("Usuário: ")
                user_password = input("Senha: ")

                server_socket.send(f"LOGIN {user_name} {user_password}".encode())
                send_input("public_key", keys["public"], "no_encode")

                response = get_messages()

                if response[0] == "0":
                    print("\nUsuário autenticado\n")
                    chat(server_socket, keys)
                else:
                    print(f"\nErro: {response[1]}\n")
                    
            case _:
                continue

        # server_socket.send(message.encode())