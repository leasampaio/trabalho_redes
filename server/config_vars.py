from crypto_methods import *

import logging

HOST = "127.0.0.2"
PORT = 5000
MAX_CONNECTIONS = 100
MAX_ROOM_CAPACITY = 10

MAIN_ROOM = "geral"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

keys = generate_keys()