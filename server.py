import socket
import threading
import hashlib
from cryptography.fernet import Fernet

# Gerar chave de criptografia
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

# Configurações do servidor
HOST = '127.0.0.1'
PORT = 5000
MAX_CONNECTIONS = 5

# Dicionário para armazenar usuários e suas conexões
usuarios = {}
conexoes = {}

def registrar_usuario(usuario, senha):
    if usuario in usuarios:
        return False
    usuarios[usuario] = hashlib.sha256(senha.encode()).hexdigest()
    return True

def autenticar_usuario(usuario, senha):
    if usuario in usuarios:
        return usuarios[usuario] == hashlib.sha256(senha.encode()).hexdigest()
    return False

def enviar_mensagem(destinatario, mensagem, remetente):
    if destinatario in conexoes:
        conexoes[destinatario].send(f"Mensagem de {remetente}: {mensagem}\n".encode('utf-8'))
        return True
    return False

def tratar_cliente(conn, addr):
    conn.send("Bem-vindo ao servidor de chat!\n".encode('utf-8'))
    usuario = None

    try:
        while True:
            conn.send("[1] Registrar\n[2] Login\nEscolha uma opção: ".encode('utf-8'))
            opcao = conn.recv(1024).decode('utf-8').strip()

            if opcao == '1':
                conn.send("Digite um nome de usuário: ".encode('utf-8'))
                usuario = conn.recv(1024).decode('utf-8').strip()
                conn.send("Digite uma senha: ".encode('utf-8'))
                senha = conn.recv(1024).decode('utf-8').strip()

                if registrar_usuario(usuario, senha):
                    conn.send("Registro bem-sucedido!\n".encode('utf-8'))
                else:
                    conn.send("Usuário já existe.\n".encode('utf-8'))

            elif opcao == '2':
                conn.send("Digite seu nome de usuário: ".encode('utf-8'))
                usuario = conn.recv(1024).decode('utf-8').strip()
                conn.send("Digite sua senha: ".encode('utf-8'))
                senha = conn.recv(1024).decode('utf-8').strip()

                if autenticar_usuario(usuario, senha):
                    conn.send("Login bem-sucedido!\n".encode('utf-8'))
                    conexoes[usuario] = conn
                    break
                else:
                    conn.send("Usuário ou senha inválidos.\n".encode('utf-8'))

        while True:
            conn.send("[1] Enviar mensagem\n[2] Sair\nEscolha uma opção: ".encode('utf-8'))
            opcao = conn.recv(1024).decode('utf-8').strip()

            if opcao == '1':
                conn.send("Digite o nome do destinatário: ".encode('utf-8'))
                destinatario = conn.recv(1024).decode('utf-8').strip()
                conn.send("Digite sua mensagem: ".encode('utf-8'))
                mensagem = conn.recv(1024).decode('utf-8').strip()

                if enviar_mensagem(destinatario, mensagem, usuario):
                    conn.send("Mensagem enviada!\n".encode('utf-8'))
                else:
                    conn.send("Usuário não encontrado ou offline.\n".encode('utf-8'))

            elif opcao == '2':
                conn.send("Desconectando...\n".encode('utf-8'))
                break

    except Exception as e:
        print(f"Erro com {addr}: {e}")
    finally:
        if usuario:
            conexoes.pop(usuario, None)
        conn.close()

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(MAX_CONNECTIONS)
    print(f"Servidor iniciado em {HOST}:{PORT}")

    while True:
        conn, addr = servidor.accept()
        threading.Thread(target=tratar_cliente, args=(conn, addr)).start()

if __name__ == "__main__":
    iniciar_servidor()