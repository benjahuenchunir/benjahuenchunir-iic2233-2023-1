import socket
import random
from threading import Thread
import Scripts.cripto as cr
from parametros import parametro
import json


class Server:
    def __init__(self, host: str, port: int):
        self.sockets = {}
        self.socket_ids = {}
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.aceptar_conexiones()
        self.codificar_mensaje(bytearray(b'\x01\x05\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04'))

    def aceptar_conexiones(self) -> None:
        thread = Thread(
            target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self) -> None:
        while len(self.sockets) < parametro("NUMERO_JUGADORES"):
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
            except ConnectionError:
                print("Ocurrió un error.")
            except KeyboardInterrupt:
                print("Interrupcion del usuario")
                break
        self.sock.close()

    def agregar_cliente(self, socket_cliente, address):
        self.sockets[socket_cliente] = address
        print(parametro("ids"))
        self.socket_ids[socket_cliente] = random.choice(list(parametro("ids").values()))
        for socket in self.sockets:
            socket.send(('agregar:' + self.socket_ids[socket_cliente]).encode('utf-8'))

    def escuchar_cliente(self, socket_cliente: socket.socket) -> None:
        while True:
            print(f"{self.sockets[socket_cliente]}")
            try:
                data = socket_cliente.recv(parametro("SIZE_BUFFER").decode("utf-8"))
                if data:
                    print("tamos bien")
                    print(data)
                    if data == parametro("USUARIO_DESCONECTADO"):
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

    def codificar_mensaje(self, mensaje: bytearray):
        encoded_chunks = bytearray(len(mensaje).to_bytes(4, 'little'))
        print(encoded_chunks)
        chunks = bytearray([mensaje[i:i+128] for i in range(0, len(mensaje), 128)])
        print(chunks)

        for i, chunk in enumerate(chunks):
            # Convertir el número de bloque a big endian (4 bytes)
            numero_chunk = i.to_bytes(4, 'big')

            # Agregar el número de bloque al inicio del chunk
            encoded_chunk = numero_chunk + chunk

            # Agregar el chunk codificado a la lista
            encoded_chunks.append(encoded_chunk)

        # Codificar la lista de chunks en JSON
        encoded_message = json.dumps(encoded_chunks)

        # Obtener la longitud de la lista de chunks codificados
        encoded_length = len(encoded_message)

        # Convertir la longitud a little endian (4 bytes)
        encoded_length_bytes = encoded_length.to_bytes(4, 'little')

        # Agregar los bytes de longitud al inicio del mensaje codificado
        encoded_message = encoded_length_bytes + encoded_message.encode('utf-8')

        return encoded_message

if __name__ == "__main__":
    host = parametro("host")
    port = int(parametro("port"))
    server = Server(host, port)
