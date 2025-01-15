import socket
import threading
import logging

HOST = "127.0.0.2"
PORT = 5000
MAX_CONNECTIONS = 5


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

users = {}


def handle_client(client_socket: socket.socket, client_address):
    logging.info(f"Conexão {client_address} estabelecida.")

    def waitFor(input_name):
        client_socket.send(f"GET {input_name}".encode())
        value = client_socket.recv(1024).decode().strip()
        return value
        
    def endMessage():
        client_socket.send("END_OF_MESSAGE".encode())

    while True:
        option = client_socket.recv(1024).decode().strip()
        logging.info(f"Mensagem {option} recebida de {client_address}.")
        
        match option:
            case "QUIT":
                break
            case "REGISTER":
                user_name = waitFor("user_name")
                user_password = waitFor("user_password")

                if user_name in users:
                    client_socket.send("1".encode())
                    client_socket.send("Usuário já cadastrado".encode())
                    endMessage()
                else:
                    client_socket.send("0".encode())
                    endMessage()

                    new_user = {
                        "password": user_password,
                        "public_key": None
                    }
                    users[user_name] = new_user

                    logging.info(f"Usuário {user_name} cadastrado.")
            case "LOGIN":
                user_name = waitFor("user_name")
                user_password = waitFor("user_password")

                if (user_name in users) and (users[user_name]["password"] == user_password):
                    client_socket.send("0".encode())
                    client_socket.send("Usuário autenticado".encode())
                    endMessage()
                else:
                    client_socket.send("1".encode())
                    client_socket.send("Usuário ou senha inválidos".encode())
                    endMessage()
            case _:
                break

    client_socket.close()
    logging.info(f"Conexão {client_address} encerrada.")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CONNECTIONS)
    
    logging.info(f"Servidor escutando em {HOST}:{PORT}.")
    
    while True:
        client_socket, client_address = server_socket.accept()
        
        client_thread = threading.Thread(target=handle_client, args=[client_socket, client_address])
        client_thread.start()

if __name__ == "__main__":
    main()