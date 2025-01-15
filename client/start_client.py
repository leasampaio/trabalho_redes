from config_vars import *
from crypto_methods import *
from chat import *

import threading

def start(server_socket):
    global server_key

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
                send("QUIT".encode())
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
                    
            case _:
                continue

        # server_socket.send(message.encode())