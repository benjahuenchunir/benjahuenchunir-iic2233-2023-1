import socket
from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread
from utils.utils import parametro, Mensaje
import backend.Scripts.cripto as cr
import pickle


class Logica(QObject):
    senal_agregar_usuario = pyqtSignal(str)
    senal_eliminar_usuario = pyqtSignal(str)

    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def conectar_servidor(self):
        try:
            self.socket_cliente.connect((self.host, self.port))
            listening_server_thread = Thread(target=self.escuchar_servidor, daemon=True)
            listening_server_thread.start()
        except ConnectionError:
            print("Conexion terminada")
            self.socket_cliente.close()
            exit()

    def escuchar_servidor(self):
        data = self.socket_cliente.recv(parametro("TAMANO_CHUNKS_BLOQUE"))
        if data:
            print(self.recibir_mensaje(data))
        else:
            print(
                "No hay info"
            )  # TODO creo que esto nunca pasa o pasa cuando se cae el server?

    def recibir_mensaje(self, data: bytes):
        largo = int.from_bytes(data, byteorder="little")
        print(largo)
        largo_total = (
            parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")
        ) * (largo // parametro("TAMANO_CHUNKS_MENSAJE") + 1)
        print(largo_total)
        bytes_mensaje = self.socket_cliente.recv(largo_total)
        mensaje_decodificado = self.decodificar_mensaje(bytes_mensaje)
        mensaje_desencriptado = cr.desencriptar(
            mensaje_decodificado, parametro("N_PONDERADOR")
        )
        mensaje = pickle.loads(mensaje_desencriptado)
        return mensaje

    def decodificar_mensaje(self, mensaje: bytes) -> bytearray:
        mensaje_decodificado = bytearray()
        for i in range(
            0,
            len(mensaje),
            parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE"),
        ):
            mensaje_decodificado.extend(
                mensaje[
                    i
                    + parametro("TAMANO_CHUNKS_BLOQUE") : i
                    + parametro("TAMANO_CHUNKS_MENSAJE") +parametro("TAMANO_CHUNKS_BLOQUE")
                ]
            )  # TODO falta revisar 0 agregados
        return mensaje_decodificado

    def codificar_mensaje(self, mensaje: bytearray) -> bytearray:
        mensaje_codificado = bytearray(
            len(mensaje).to_bytes(parametro("TAMANO_CHUNKS_BLOQUE"), "little")
        )
        for i in range(0, len(mensaje), parametro("TAMANO_CHUNKS_MENSAJE")):
            mensaje_codificado.extend(
                i.to_bytes(parametro("TAMANO_CHUNKS_BLOQUE"), "big")
            )
            chunk = mensaje[i : i + parametro("TAMANO_CHUNKS_MENSAJE")]
            if len(chunk) < parametro("TAMANO_CHUNKS_MENSAJE"):
                print(
                    "Agregando",
                    parametro("TAMANO_CHUNKS_MENSAJE") - len(chunk),
                    "ceros",
                )
                chunk.extend(bytearray(parametro("TAMANO_CHUNKS_MENSAJE") - len(chunk)))
            mensaje_codificado.extend(chunk)
        print(mensaje_codificado)
        return mensaje_codificado

    def mandar_mensaje(self, mensaje: Mensaje):
        bytes_mensaje = pickle.dumps(mensaje)
        print("El mansaje que se esta mandando es:", bytes_mensaje)
        mensaje_encriptado = cr.encriptar(bytes_mensaje, parametro("N_PONDERADOR"))
        print("Mensaje encriptado", mensaje_encriptado)
        mensaje_codificado = self.codificar_mensaje(mensaje_encriptado)
        print("Mensaje codificado", mensaje_codificado)
        print("Enviando mensaje")
        self.socket_cliente.sendall(mensaje_codificado)
        print("Mensaje enviado")

    def test_manejar_mensaje(self): #Mensaje exacto
        mensaje = Mensaje("comenzar", "ajdhasdhñashidoasjdoasidjasidjaosaaaaaaaaaaaaaaa")
        self.mandar_mensaje(mensaje)

    def test_manejar_mensaje2(self):
        mensaje = Mensaje("eliminar", "xd")
        self.mandar_mensaje(mensaje)
