from memory_data import *
from crypto_methods import *

def send_message(user, message):
    encrypted = encrypt(user["public_key"], message)
    user["client_socket"].send(encrypted)

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
            "users": [],
            "owner": user
        }

    rooms[room_name]["users"].append(user)

    online_users = len(rooms[room_name]["users"])
    online_users_text = "Você é o único usuário nesta sala." if online_users <= 1 else "Estão online aqui: " + ", ".join([u["name"] for u in rooms[room_name]["users"]])

    broadcast(room_name, f"{user['name']} entrou na sala.", exclude_user=user)
    send_message(user, f"Você entrou na sala {room_name}. {online_users_text}")

def log_out(user):
    logging.info(f"{user["name"]} foi desconectado.")
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
        send_message(user, "Usuário não encontrado")
        return

    user["reply_to"] = target_user
    target_user["reply_to"] = user

    send_message(target_user, f"{user['name']} sussurrou: {message}")
    send_message(user, f">> p/ {target_user_name}: {message}")

def reply(user, message):
    whisper(user, user["reply_to"]["name"], message)

def broadcast(room_name, message, exclude_user=None):
    for user in rooms[room_name]["users"]:
        if user["name"] != exclude_user["name"]:
            print (f"Enviando mensagem para {user['name']}: {message}")
            try:
                send_message(user, message)
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

        encrypted = client_socket.recv(1024)
        message = decrypt(keys["private"], encrypted).strip()

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
                    send(user, "Comando inválido")
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
                send_message(user, "Comando inválido")
        else:
            logging.info(f"Mensagem \"{message}\" enviada por {user['name']}.")
            broadcast(user["room"], f"{user['name']}: {message}", exclude_user=user)