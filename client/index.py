from start_client import *

import threading
import socket
import traceback 

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

if __name__ == "__main__":
    main()
