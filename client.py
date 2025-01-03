# TODO
#  - conexao com o servidor para implementar as funcionalidades e requisitos do projeto

# - cada cliente se comunica com o servidor, que gerenciara a comunicacao entre clientes
# - cada cliente deve se cadastrar junto ao servidor como um usuario
# - cada cliente deve poder se comunicar com outro cliente usando o nome de usuario (semelhante ao que ocorre no WhatsApp atraves do numero de telefone)
# - (OPCIONAL) clientes podem se juntar a grupos multicast (semelhante ao que ocorre no whatsapp)




import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

def receber_mensagens(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024).decode('utf-8')
            print(mensagem)
        except:
            print("Conexão encerrada.")
            break

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    threading.Thread(target=receber_mensagens, args=(cliente,)).start()

    while True:
        try:
            mensagem = input()
            cliente.send(mensagem.encode('utf-8'))
            if mensagem.lower() == 'sair':
                break
        except Exception as e:
            print(f"Erro: {e}")
            break

    cliente.close()

if __name__ == "__main__":
    iniciar_cliente()