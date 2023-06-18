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
        #self.codificar_mensaje(bytearray(b'\x01\x05\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04'))

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
        return
        """for socket in self.sockets:
            socket.send(('agregar:' + self.socket_ids[socket_cliente]).encode('utf-8'))"""

    def escuchar_cliente(self, socket_cliente: socket.socket) -> None:
        while True:
            print(f"{self.sockets[socket_cliente]}")
            try:
                data = socket_cliente.recv(parametro("TAMANO_CHUNKS_BLOQUE"))
                if data:
                    print("Recibiendo mensaje de un cliente")
                    self.recibir_mensaje(socket_cliente, data)
                    print(Mensaje)
                else:
                    print("Usuario desconectado")
                    del self.sockets[socket_cliente]
                    break
            except Exception:
                # Ante cualquier error, se acaba la conexión
                # En este caso, se termina el thread que mantenía la conexión
                # con el socket de un cliente
                print("Hubo algun error")
                #break

    def recibir_mensaje(self, socket_cliente: socket.socket, data: bytes) -> Mensaje:
        largo = int.from_bytes(data, byteorder='little')
        print("El largo es", largo)
        largo_total = (parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")) * (largo // parametro("TAMANO_CHUNKS_MENSAJE"))
        print("El largo del mensaje total es", largo_total)
        bytes_mensaje = socket_cliente.recv(largo_total)
        print("Los bytes recibidos son", bytes_mensaje)
        mensaje_decodificado = self.decodificar_mensaje(bytes_mensaje)
        print("El mensaje decodificado es", mensaje_decodificado)
        print(type(mensaje_decodificado))
        print(type(parametro("N_PONDERADOR")))
        mensaje_desencriptado = self.desencriptar(mensaje_decodificado, parametro("N_PONDERADOR"))
        print("El mensaje desencriptado es", mensaje_desencriptado)
        mensaje = pickle.loads(mensaje_desencriptado)
        return mensaje
    
    def desencriptar(self, msg: bytearray, N: int) -> bytearray:
        print("Entre aca")
        msg[N], msg[0] = msg[0], msg[N],
        print("Aca mori")
        bytearray_desencriptado = bytearray(msg)
        for y in range(len(msg)):
            bytearray_desencriptado[y] = msg[(y + N) % len(msg)]
        print("Mentira")
        return bytearray_desencriptado

    def decodificar_mensaje(self, mensaje: bytes) -> bytearray:
        mensaje_decodificado = bytearray()
        for i in range(0, len(mensaje), parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")):
            print(len(mensaje[i+parametro("TAMANO_CHUNKS_BLOQUE"):i+parametro("TAMANO_CHUNKS_MENSAJE")]))
            print(mensaje[i+parametro("TAMANO_CHUNKS_BLOQUE"):+ parametro("TAMANO_CHUNKS_MENSAJE")+parametro("TAMANO_CHUNKS_BLOQUE")])
            mensaje_decodificado.extend(mensaje[i+parametro("TAMANO_CHUNKS_BLOQUE"):i+parametro("TAMANO_CHUNKS_MENSAJE")+parametro("TAMANO_CHUNKS_BLOQUE")]) # TODO falta revisar 0 agregados
        return mensaje_decodificado

    def codificar_mensaje(self, mensaje: bytearray):
        mensaje_codificado = bytearray(len(mensaje).to_bytes(
            parametro("TAMANO_CHUNKS_BLOQUE"), 'little'))
        for i in range(0, len(mensaje), parametro("TAMANO_CHUNKS_MENSAJE")):
            mensaje_codificado.extend(i.to_bytes(
                parametro("TAMANO_CHUNKS_BLOQUE"), 'big'))
            chunk = mensaje[i:i+parametro("TAMANO_CHUNKS_MENSAJE")]
            if len(chunk) < parametro("TAMANO_CHUNKS_MENSAJE"):
                chunk.extend(bytearray(
                    parametro("TAMANO_CHUNKS_MENSAJE") - len(chunk)))
            mensaje_codificado.extend(chunk)
        print(mensaje_codificado)
        return mensaje_codificado

    def mandar_mensaje(self, mensaje: str):
        mensaje_encriptado = cr.encriptar(bytearray(mensaje), parametro("N_PONDERADOR"))
        mensaje_codificado = self.codificar_mensaje(mensaje_encriptado)
        for socket in self.sockets:
            socket.sendall(mensaje_codificado)


if __name__ == "__main__":
    host = parametro("host")
    port = parametro("port")
    server = Server(host, port)
