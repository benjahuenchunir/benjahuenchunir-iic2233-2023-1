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
        self.id = None

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
        while True:
            data = self.socket_cliente.recv(parametro("TAMANO_CHUNKS_BLOQUE"))
            if data:
                mensaje = self.recibir_mensaje(data)
                print(mensaje)
                self.manejar_mensaje(mensaje)
            else:
                print(
                    "No hay info"
                )  # TODO creo que esto nunca pasa o pasa cuando se cae el server?
                
    def manejar_mensaje(self, mensaje: Mensaje):
        if mensaje.operacion == parametro("OP_ASIGNAR_NOMBRE"):
            print(mensaje.data)
            self.id = mensaje.data
        elif mensaje.operacion == parametro("OP_AGREGAR_USUARIO"):
            print("Agregando a:", mensaje.data)
            self.senal_agregar_usuario.emit(mensaje.data)

    def recibir_mensaje(self, data: bytes) -> Mensaje:
        largo = int.from_bytes(data, byteorder='little')
        largo_total = (parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")) * (largo // parametro("TAMANO_CHUNKS_MENSAJE") + min(1, largo % parametro("TAMANO_CHUNKS_MENSAJE")))
        bytes_mensaje = self.socket_cliente.recv(largo_total)
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
            len(mensaje).to_bytes(parametro("TAMANO_CHUNKS_BLOQUE"), "little")
        )
        for i in range(0, len(mensaje), parametro("TAMANO_CHUNKS_MENSAJE")):
            mensaje_codificado.extend(
                i.to_bytes(parametro("TAMANO_CHUNKS_BLOQUE"), "big"))
            chunk = mensaje[i: i + parametro("TAMANO_CHUNKS_MENSAJE")]
            if len(chunk) < parametro("TAMANO_CHUNKS_MENSAJE"):
                chunk.extend(
                    bytearray(parametro("TAMANO_CHUNKS_MENSAJE") - len(chunk)))
            mensaje_codificado.extend(chunk)
        return mensaje_codificado

    def mandar_mensaje(self, mensaje: Mensaje):
        bytes_mensaje = pickle.dumps(mensaje)
        mensaje_encriptado = cr.encriptar(bytes_mensaje, parametro("N_PONDERADOR"))
        mensaje_codificado = self.codificar_mensaje(mensaje_encriptado)
        self.socket_cliente.sendall(mensaje_codificado)

    def test_manejar_mensaje(self): #Mensaje exacto
        mensaje = Mensaje("comenzar", "ajdhasdhñashidoasjdoasidjasidjaosaaaaaaaaaaaaaaa")
        self.mandar_mensaje(mensaje)

    def test_manejar_mensaje2(self):
        mensaje = Mensaje("eliminar", "xd")
        self.mandar_mensaje(mensaje)
