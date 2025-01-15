from memory_data import *

def create_user(user_name, user_password, client_socket):
    new_user = {
        "name": user_name,
        "password": user_password,
        "public_key": None,
        "room": MAIN_ROOM,
        "client_socket": client_socket,
        "reply_to": None
    }
    users[user_name] = new_user

def join_room(user, room_name):
    old_room = user["room"]
    
    if user in rooms[old_room]["users"]:
        rooms[old_room]["users"].remove(user)

    user["room"] = room_name

    if room_name not in rooms:
        rooms[room_name] = {
            "users": [user],
            "owner": user
        }
    else:
        rooms[room_name]["users"].append(user)

    broadcast(room_name, f"{user['name']} entrou na sala.", exclude_user=user)
    user["client_socket"].send(f"Você entrou na sala {room_name}".encode())

def log_out(user):
    if user in rooms[user["room"]]["users"]:
        rooms[user["room"]]["users"].remove(user)
    try:
        user["client_socket"].close()
        user["client_socket"] = None
    except:
        pass

def whisper(user, target_user_name, message):
    target_user = users[target_user_name]
    if not target_user:
        user["client_socket"].send("Usuário não encontrado".encode())
        return

    target_user["reply_to"] = user
    target_user["client_socket"].send(f"{user['name']} sussurrou: {message}".encode())
    user["client_socket"].send(f"<<p/ {target_user_name}>>: {message}".encode())

def reply(user, message):
    whisper(user, user["reply_to"]["name"], message)

def broadcast(room_name, message, exclude_user=None):
    for user in rooms[room_name]["users"]:
        if user["name"] != exclude_user["name"]:
            print (f"Enviando mensagem para {user['name']}: {message}")
            try:
                user["client_socket"].send(message.encode())
            except Exception as e:
                logging.error(f"Erro ao enviar mensagem para {user['name']}: {e}")
                log_out(user)

def chat(user):
    while True:
        room = rooms[user["room"]]
        client_socket = user["client_socket"]

        if not room:
            logging.error(f"Sala {user['room']} não existe.")
            return

        message = client_socket.recv(1024).decode().strip()

        if not message:
            log_out(user)
            return
        elif message.startswith("/"):
            command = message.split(" ")[0].lower()
            args = message.split(" ")[1:]

            if command == "/j" or command == "/join":
                new_room = args[0]
                join_room(user, new_room)

            elif command == "/l" or command == "/leave":
                join_room(user, MAIN_ROOM)

            elif command == "/w" or command == "/whisper":
                if (len(args) < 2):
                    client_socket.send("Comando inválido".encode())
                    continue
                target_user_name = args[0]
                message = " ".join(args[1:])
                whisper(user, target_user_name, message)
                return

            elif command == "/r" or command == "/reply":
                message = " ".join(args)
                reply(user, message)
                return

            else:
                client_socket.send("Comando inválido".encode())
        else:
            logging.info(f"Mensagem \"{message}\" enviada por {user['name']}.")
            broadcast(user["room"], f"{user['name']}: {message}", exclude_user=user)