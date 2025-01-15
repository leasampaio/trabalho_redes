import threading
import socket



def handle_messages(server_socket: socket.socket):
    ...


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_host = "127.0.0.2"
    server_port = 5000

    server_socket.connect((server_host, server_port))

    print()
    print("Conexão com o servidor estabelecida!")
    print()

    threading.Thread(target=handle_messages, args=[server_socket]).start()
    
    
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
                user_name = input("Usuário: ")
                user_password = input("Senha: ")
                server_socket.send("SUBSCRIBE".encode())
                server_socket.send(user_name.encode())
                server_socket.send(user_password.encode())
                
                response = server_socket.recv(1024).decode().strip()
                if response == "1":
                    response = server_socket.recv(1024).decode().strip()
                    print(f"Erro: {response}")
                else:
                    print("Usuário cadastrado com sucesso")
            case _:
                continue
                
        
        # server_socket.send(message.encode())

    server_socket.close()


if __name__ == "__main__":
    main()
