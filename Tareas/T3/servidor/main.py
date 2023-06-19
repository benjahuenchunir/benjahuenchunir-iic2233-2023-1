import socket
import random
from threading import Thread
import Scripts.cripto as cr
from utils.utils import parametro, Mensaje
import pickle


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

    def aceptar_conexiones(self) -> None:
        thread = Thread(
            target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self) -> None:
        while True:
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
                self.sock.close()
                break
        print("Cerrando server")
        self.sock.close()

    def agregar_cliente(self, socket_cliente, address) -> str:
        self.sockets[socket_cliente] = address
        print(parametro("ids"))
        id = random.choice([nombre for nombre in parametro("ids").values() if nombre not in self.socket_ids.values()])
        print(id)
        self.socket_ids[socket_cliente] = id
        self.mandar_mensaje(Mensaje(parametro("OP_ASIGNAR_NOMBRE"), id), socket_cliente)
        self.mandar_mensaje(Mensaje(parametro("OP_AGREGAR_USUARIOS"), [usuario for usuario in self.socket_ids.values() if usuario != id]), socket_cliente)
        self.mandar_mensaje_a_todos(Mensaje(parametro("OP_AGREGAR_USUARIO"), id))

    def escuchar_cliente(self, socket_cliente: socket.socket) -> None:
        while True:
            print(f"{self.sockets[socket_cliente]}")
            try:
                data = socket_cliente.recv(parametro("TAMANO_CHUNKS_BLOQUE"))
                if len(data) > 0:
                    print("Recibiendo mensaje de un cliente")
                    mensaje = self.recibir_mensaje(socket_cliente, data)
                    print(mensaje)
                else:
                    print("Usuario desconectado")
                    self.eliminar_cliente(socket_cliente) # TODO esto no se llama sino que si el usuario se va tira exception
                    break
            except Exception:
                print("Hubo algun error")
                self.eliminar_cliente(socket_cliente)
                break

    def eliminar_cliente(self, socket_cliente):
        print("ELiminando cliente")
        del self.sockets[socket_cliente]
        self.mandar_mensaje_a_todos(Mensaje(parametro("OP_ELIMINAR_USUARIO"), self.socket_ids[socket_cliente]))
        del self.socket_ids[socket_cliente]
        print("Cliente eliminado")

    def recibir_mensaje(self, socket_cliente: socket.socket, data: bytes) -> Mensaje:
        largo = int.from_bytes(data, byteorder='little')
        largo_total = (parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")) * (largo // parametro("TAMANO_CHUNKS_MENSAJE") + min(1, largo % parametro("TAMANO_CHUNKS_MENSAJE")))
        bytes_mensaje = socket_cliente.recv(largo_total)
        mensaje_decodificado = self.decodificar_mensaje(bytes_mensaje, largo)
        mensaje_desencriptado = cr.desencriptar(mensaje_decodificado, parametro("N_PONDERADOR"))
        mensaje = pickle.loads(mensaje_desencriptado)
        return mensaje

    def decodificar_mensaje(self, mensaje: bytes, largo: int) -> bytearray:
        mensaje_decodificado = bytearray()
        for i in range(0, len(mensaje) - (parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")), parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")):
            mensaje_decodificado.extend(mensaje[i+parametro("TAMANO_CHUNKS_BLOQUE"):i+parametro("TAMANO_CHUNKS_MENSAJE")+parametro("TAMANO_CHUNKS_BLOQUE")])
        mensaje_decodificado.extend(mensaje[-parametro("TAMANO_CHUNKS_MENSAJE"):][:largo])
        return mensaje_decodificado

    def codificar_mensaje(self, mensaje: bytearray) -> bytearray:
        mensaje_codificado = bytearray(
            len(mensaje).to_bytes(parametro("TAMANO_CHUNKS_BLOQUE"), "little"))
        for i in range(0, len(mensaje), parametro("TAMANO_CHUNKS_MENSAJE")):
            mensaje_codificado.extend(
                i.to_bytes(parametro("TAMANO_CHUNKS_BLOQUE"), "big"))
            chunk = mensaje[i: i + parametro("TAMANO_CHUNKS_MENSAJE")]
            if len(chunk) < parametro("TAMANO_CHUNKS_MENSAJE"):
                chunk.extend(
                    bytearray(parametro("TAMANO_CHUNKS_MENSAJE") - len(chunk)))
            mensaje_codificado.extend(chunk)
        return mensaje_codificado

    def convertir_mensaje(self, mensaje: Mensaje):
        bytes_mensaje = pickle.dumps(mensaje)
        mensaje_encriptado = cr.encriptar(bytes_mensaje, parametro("N_PONDERADOR"))
        return self.codificar_mensaje(mensaje_encriptado)

    def mandar_mensaje_a_todos(self, mensaje: Mensaje,):
        mensaje_codificado = self.convertir_mensaje(mensaje)
        for socket in self.sockets:
            socket.sendall(mensaje_codificado)

    def mandar_mensaje(self, mensaje: Mensaje, socket_cliente: socket.socket):
        mensaje_codificado = self.convertir_mensaje(mensaje)
        socket_cliente.sendall(mensaje_codificado)


if __name__ == "__main__":
    host = parametro("host")
    port = parametro("port")
    server = Server(host, port)
