import threading
import socket
import crypto
import traceback 

HOST = "127.0.0.2"
PORT = 5000

def handle_messages(server_socket: socket.socket):
    ...

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        start(server_socket)
    except Exception as e:
        print(f"Erro: {e}")
        traceback.print_exc() 
    finally:
        print("Encerrando cliente...")
        server_socket.close()

def start(server_socket):

    server_socket.connect((HOST, PORT))

    print()
    print("Conexão com o servidor estabelecida!")
    print()

    threading.Thread(target=handle_messages, args=[server_socket]).start()

    def getMessages():
        messages = []
        while True:
            message = server_socket.recv(1024).decode().strip()
            if message != "END_OF_MESSAGE":
                messages.append(message)
            else:
                return messages

    def sendInput(key, value, no_encode=""):
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

                server_socket.send("REGISTER".encode())
                sendInput("user_name", user_name)
                sendInput("user_password", user_password)

                response = getMessages(server_socket)

                if response[0] == "0":
                    print("\nUsuário cadastrado com sucesso\n")
                else:
                    print(f"\nErro: {response[1]}\n")

            case "2":
                print("\n")
                keys = crypto.generate_keys()

                user_name = input("Usuário: ")
                user_password = input("Senha: ")

                server_socket.send("LOGIN".encode())
                sendInput("user_name", user_name)
                sendInput("user_password", user_password)
                sendInput("public_key", keys["public"], "no_encode")

                response = getMessages(server_socket)

                if response[0] == "0":
                    print("\nUsuário autenticado\n")
                    chat(server_socket, keys)
                else:
                    print(f"\nErro: {response}\n")
                    
            case _:
                continue

        # server_socket.send(message.encode())


def chat(server_socket, keys):
    while True:
        message = input("> ")
        print(f"<Você> {message}")

if __name__ == "__main__":
    main()
