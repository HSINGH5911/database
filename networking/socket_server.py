import socket
import threading

from core.database import Database
from commands.registry import execute

HOST = "127.0.0.1"
PORT = 6379

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()

print(f"Listening on {HOST}:{PORT}")

db = Database()



def handle_client(client):
    while True:

        client, address = server.accept()

        print(f"Connected: {address}")

        data = client.recv(1024)

        if not data:
            break

        message = data.decode().strip()

        parts = message.split()

        command = parts[0]
        args = parts[1:]

        result = execute(command, db, args)

        client.send(str(result).encode())