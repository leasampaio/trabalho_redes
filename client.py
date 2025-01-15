
import os
import socket
import threading
import crypto

chaves = {}

HOST = '127.0.0.1'
PORT = 5000
UDP_PORT = 5001

def receber_mensagens(cliente):
    global chaves
    
    while True:
        plaintext = cliente.recv(1024)
        try:
            mensagem = plaintext.decode('utf-8')
            if (mensagem == "GET_KEY"):
                chaves = crypto.generate_keys()
                cliente.send(chaves["public"])
            else:
                print(mensagem)
        except Exception as e:
            try:
                mensagem = crypto.decrypt(chaves["private"], plaintext)
                print(mensagem)
            except Exception as e:
                print(f"Conexão encerrada: {e}")
            break

def enviar_arquivo_udp(nome_arquivo):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    with open(nome_arquivo, "rb") as f:
        while (dados := f.read(4096)):
            udp_socket.sendto(dados, (HOST, UDP_PORT))

    udp_socket.close()

def iniciar_cliente():
    global chaves

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    threading.Thread(target=receber_mensagens, args=(cliente,)).start()

    while True:
        try:
            mensagem = input()
            if mensagem.lower() == 'sair':
                break

            cliente.send(mensagem.encode('utf-8'))
        except Exception as e:
            print(f"Erro: {e}")
            break

    cliente.close()

if __name__ == "__main__":
    iniciar_cliente()