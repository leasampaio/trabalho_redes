from start_client import *

import threading
import socket
import traceback 
import time

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        start(server_socket)
    except Exception as e:
        print(f"Erro: {e}")
        server_socket.close()
        print("Conexão com o servidor perdida!")
        time.sleep(1)
        print("Reconectando...")
        main() 

if __name__ == "__main__":
    main()
