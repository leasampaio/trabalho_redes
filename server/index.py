from config_vars import *
from user_actions import *
from user_socket import *

import socket
import threading
import logging

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