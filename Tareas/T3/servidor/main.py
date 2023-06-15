import socket
import random
from threading import Thread
import json


class Server:
    def __init__(self, host: str, port: int, parametros):
        self.sockets = {}
        self.socket_ids = {}
        self.host = host
        self.port = port
        self.parametros = parametros
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.aceptar_conexiones()

    def aceptar_conexiones(self) -> None:
        thread = Thread(
            target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self) -> None:
        counter = 0
        while counter < data["MAXIMO_JUGADORES"]:
            try:
                print("Esperando que alguien se quiera conectar...")
                socket_cliente, address = self.sock.accept()
                print("Conexión aceptada desde", address)
                self.agregar_cliente(socket_cliente, address)
                listening_client_thread = Thread(
                    target=self.escuchar_cliente,
                    args=(socket_cliente, ),
                    daemon=True)
                listening_client_thread.start()
                counter += 1
            except ConnectionError:
                print("Ocurrió un error.")
            except KeyboardInterrupt:
                print("Interrupcion del usuario")
        self.sock.close()

    def agregar_cliente(self, socket_cliente, address):
        self.sockets[socket_cliente] = address
        print(self.parametros["ids"])
        self.socket_ids[socket_cliente] = random.choice(list(self.parametros["ids"].values()))
        for socket in self.sockets:
            socket.send(('agregar:' + self.socket_ids[socket_cliente]).encode('utf-8'))

    def escuchar_cliente(self, socket_cliente: socket.socket) -> None:
        while True:
            print(f"{self.sockets[socket_cliente]}")
            try:
                data = socket_cliente.recv(self.parametros["SIZE_BUFFER"]).decode("utf-8")
                if data:
                    print("tamos bien")
                    print(data)
                    if data == self.parametros["USUARIO_DESCONECTADO"]:
                        self.manejar_mensaje(data, socket_cliente)
                else:
                    print("Usuario desconectado")
                    return
            except Exception:
                # Ante cualquier error, se acaba la conexión
                # En este caso, se termina el thread que mantenía la conexión
                # con el socket de un cliente
                print("Hubo algun error")
                return

    def manejar_mensaje(self, mensaje, socket_cliente):
        if mensaje == 'continuar':
            print("Continuar")
        elif mensaje == 'salir':
            print("salir")
            self.eliminar_usuario(socket_cliente)
            
    def eliminar_usuario(self, socket_cliente):
        for sockets in socket_cliente:
            pass
            


if __name__ == "__main__":
    with open("parametros.json", "rt", encoding="utf-8") as f: # TODO encoding
        data = json.loads(f.read())
    host = data["host"]
    port = int(data["port"])
    server = Server(host, port, data)
