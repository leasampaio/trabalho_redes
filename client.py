# TODO
#  - conexao com o servidor para implementar as funcionalidades e requisitos do projeto

# - cada cliente se comunica com o servidor, que gerenciara a comunicacao entre clientes
# - cada cliente deve se cadastrar junto ao servidor como um usuario
# - cada cliente deve poder se comunicar com outro cliente usando o nome de usuario (semelhante ao que ocorre no WhatsApp atraves do numero de telefone)
# - (OPCIONAL) clientes podem se juntar a grupos multicast (semelhante ao que ocorre no whatsapp)

import socket
import threading
import crypto

chaves = {}

HOST = '127.0.0.1'
PORT = 5000

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