import socket
import threading
import logging

HOST = "127.0.0.2"
PORT = 5000
MAX_CONNECTIONS = 5


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

users: dict[str, str] = {}


def handle_client(client_socket: socket.socket, client_address):
    logging.info(f"Conexão {client_address} estabelecida.")
    
    while True:
        option = client_socket.recv(1024).decode().strip()
        logging.info(f"Mensagem {option} recebida de {client_address}.")
        
        match option:
            case "QUIT":
                break
            case "SUBSCRIBE":
                user_name = client_socket.recv(1024).decode().strip()
                user_password = client_socket.recv(1024).decode().strip()
                
                if user_name in users:
                    client_socket.send("1".encode())
                    client_socket.send("Usuário já cadastrado".encode())
                else:
                    client_socket.send("0".encode())
                    users[user_name] = user_password
            case _:
                continue

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