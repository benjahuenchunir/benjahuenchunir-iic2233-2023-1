import socket
from random import choice
from threading import Thread
import json

with open("parametros.json", "rb") as f: # TODO encoding
    data = json.loads(f.read())

host = data["host"]
port = int(data["port"])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen()

if __name__ == "__main__":
    counter = 0
    while counter < 5:
        try:
            print("Esperando que alguien se quiera conectar...")
            socket_cliente, address = sock.accept()
            print("Conexión aceptada desde", address)
            counter += 1
        except ConnectionError:
            print("Ocurrió un error.")

    sock.close()
