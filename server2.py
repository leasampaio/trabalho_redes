import socket
import threading
import logging

HOST = "127.0.0.2"
PORT = 5000
MAX_CONNECTIONS = 5


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

users = {}

def handle_client(client_socket: socket.socket, client_address):
    try:
        handle_client_unsafely(client_socket, client_address)
    except Exception as e:
        logging.error(f"Erro: {e}")
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
        option = client_socket.recv(1024).decode().strip()
        logging.info(f"Mensagem {option} recebida de {client_address}.")
        
        match option:
            case "QUIT":
                break
            case "REGISTER":
                user_name = waitFor("user_name")
                user_password = waitFor("user_password")

                if " " in user_name:
                    send("1")
                    send("Nome de usuário não pode conter espaços")
                    endMessage()
                elif user_name in users:
                    send("1")
                    send("Usuário já cadastrado")
                    endMessage()
                else:
                    send("0")
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
                public_key = waitFor("public_key")

                if (user_name in users) and (users[user_name]["password"] == user_password):
                    users[user_name]["public_key"] = public_key
                    send("0")
                    send("Usuário autenticado")
                    endMessage()
                else:
                    send("1")
                    send("Usuário ou senha inválidos")
                    endMessage()
            case "":
                break
            case _:
                continue

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CONNECTIONS)

    try:
        start(server_socket)
    except Exception as e:
        logging.error(f"Erro: {e}")
    finally:
        logging.info("Encerrando servidor...")
        server_socket.close()

def start(server_socket):    
    logging.info(f"Servidor escutando em {HOST}:{PORT}.")
    
    while True:
        client_socket, client_address = server_socket.accept()
        
        client_thread = threading.Thread(target=handle_client, args=[client_socket, client_address])
        client_thread.start()

if __name__ == "__main__":
    main()