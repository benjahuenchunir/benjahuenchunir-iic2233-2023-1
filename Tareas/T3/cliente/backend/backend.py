import socket
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from threading import Thread, Lock
from utils.utils import parametro, Mensaje
import backend.Scripts.cripto as cr
import pickle


class Logica(QObject):
    senal_actualizar_clientes = pyqtSignal(list)
    senal_servidor_cerrado = pyqtSignal(str)
    senal_empezar_juego = pyqtSignal(list)
    senal_cambiar_dados = pyqtSignal(tuple)
    senal_cambiar_numero_mayor = pyqtSignal(str)
    senal_actualizar_turnos = pyqtSignal(tuple)
    senal_mostrar_dados = pyqtSignal(list)
    senal_cambiar_vida = pyqtSignal(tuple)
    senal_ocultar_dados = pyqtSignal(list)
    senal_perder = pyqtSignal()
    senal_ganar = pyqtSignal()
    senal_emitir_alerta = pyqtSignal(str)
    senal_elegir_usuario = pyqtSignal(list)

    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.id = None
        self.pressed_keys = []
        self.pickle_lock = Lock()

    def conectar_servidor(self):
        try:
            self.socket_cliente.connect((self.host, self.port))
            listening_server_thread = Thread(target=self.escuchar_servidor, daemon=True)
            listening_server_thread.start()
        except ConnectionError:
            self.socket_cliente.close()
            exit()

    def escuchar_servidor(self):
        try:
            while True:
                data = self.socket_cliente.recv(parametro("TAMANO_CHUNKS_BLOQUE"))
                if data:
                    mensaje = self.recibir_mensaje(data)
                    self.manejar_mensaje(mensaje)
                else:
                    self.senal_servidor_cerrado.emit("El servidor se cerró")
                    break
        except ConnectionError:
            self.senal_servidor_cerrado.emit("El servidor se cerró")

    def manejar_mensaje(self, mensaje: Mensaje):
        if mensaje == parametro("OP_ASIGNAR_NOMBRE"):
            self.id = mensaje.data
        elif mensaje == parametro("OP_SALA_LLENA"):
            self.senal_emitir_alerta.emit(parametro("OP_SALA_LLENA"))
        elif mensaje == parametro("OP_PARTIDA_EN_CURSO"):
            self.senal_emitir_alerta.emit(parametro("OP_PARTIDA_EN_CURSO"))
        elif mensaje == parametro("OP_ACTUALIZAR_CLIENTES"):
            self.senal_actualizar_clientes.emit(mensaje.data)
        elif mensaje == parametro("OP_AGREGAR_JUGADORES"):
            self.senal_empezar_juego.emit(mensaje.data)
        elif mensaje == parametro("OP_CAMBIAR_DADOS"):
            self.senal_cambiar_dados.emit((self.id, mensaje.data))
        elif mensaje == parametro("OP_CAMBIAR_NUMERO_MAYOR"):
            self.senal_cambiar_numero_mayor.emit(mensaje.data)
        elif mensaje == parametro("OP_CAMBIAR_TURNOS"):
            self.senal_actualizar_turnos.emit(mensaje.data)
        elif mensaje == parametro("OP_MOSTRAR_DADOS"):
            self.senal_mostrar_dados.emit(mensaje.data)
        elif mensaje == parametro("OP_ACTUALIZAR_VIDA"):
            self.senal_cambiar_vida.emit(mensaje.data)
        elif mensaje == parametro("OP_OCULTAR_DADOS"):
            self.senal_ocultar_dados.emit(mensaje.data)
        elif mensaje == parametro("OP_PERDER"):
            self.senal_perder.emit()
        elif mensaje == parametro("OP_GANAR"):
            self.senal_ganar.emit()
        elif mensaje == parametro("OP_ELEGIR_USUARIO"):
            self.senal_elegir_usuario.emit(mensaje.data)

    def recibir_mensaje(self, data: bytes) -> Mensaje:
        largo = int.from_bytes(data, byteorder="little")
        largo_total = (
            parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")
        ) * (
            largo // parametro("TAMANO_CHUNKS_MENSAJE")
            + min(1, largo % parametro("TAMANO_CHUNKS_MENSAJE"))
        )
        bytes_mensaje = self.socket_cliente.recv(largo_total)
        mensaje_decodificado = self.decodificar_mensaje(bytes_mensaje, largo)
        mensaje_desencriptado = cr.desencriptar(
            mensaje_decodificado, parametro("N_PONDERADOR")
        )
        with self.pickle_lock:
            mensaje = pickle.loads(mensaje_desencriptado)
        return mensaje

    def decodificar_mensaje(self, mensaje: bytes, largo: int) -> bytearray:
        mensaje_decodificado = bytearray()
        for i in range(
            0,
            len(mensaje)
            - (parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")),
            parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE"),
        ):
            mensaje_decodificado.extend(
                mensaje[
                    i
                    + parametro("TAMANO_CHUNKS_BLOQUE") : i
                    + parametro("TAMANO_CHUNKS_MENSAJE")
                    + parametro("TAMANO_CHUNKS_BLOQUE")
                ]
            )
        mensaje_decodificado.extend(
            mensaje[-parametro("TAMANO_CHUNKS_MENSAJE") :][
                : largo
                - (parametro("TAMANO_CHUNKS_MENSAJE"))
                * (largo // parametro("TAMANO_CHUNKS_MENSAJE"))
            ]
        )
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
                chunk.extend(bytearray(parametro("TAMANO_CHUNKS_MENSAJE") - len(chunk)))
            mensaje_codificado.extend(chunk)
        return mensaje_codificado

    def mandar_mensaje(self, llave, data=None):
        mensaje = Mensaje(llave, data)
        with self.pickle_lock:
            bytes_mensaje = pickle.dumps(mensaje)
        mensaje_encriptado = cr.encriptar(bytes_mensaje, parametro("N_PONDERADOR"))
        mensaje_codificado = self.codificar_mensaje(mensaje_encriptado)
        self.socket_cliente.sendall(mensaje_codificado)

    def empezar_partida(self):  # Mensaje exacto
        self.mandar_mensaje(parametro("OP_COMENZAR_PARTIDA"))

    def test_manejar_mensaje2(self):
        mensaje = Mensaje("eliminar", "xd")
        self.mandar_mensaje(mensaje)

    def enviar_anunciar_valor(self, valor: str):
        self.mandar_mensaje(parametro("AC_ANUNCIAR_VALOR"), valor)

    def enviar_pasar(self):
        self.mandar_mensaje(parametro("AC_PASAR_TURNO"))

    def enviar_cambiar_dados(self):
        self.mandar_mensaje(parametro("AC_CAMBIAR_DADOS"))

    def enviar_usar_poder(self):
        self.mandar_mensaje(parametro("AC_USAR_PODER"))

    def enviar_dudar(self):
        self.mandar_mensaje(parametro("AC_DUDAR"))

    def manejar_key_pressed(self, key):
        self.pressed_keys.append(key)
        if len(self.pressed_keys) > 3:
            self.pressed_keys.pop(0)
        if self.pressed_keys == [Qt.Key_S, Qt.Key_E, Qt.Key_E]:
            self.mandar_mensaje(parametro("AC_SEE"))

    def mandar_seleccion_usario(self, usuario):
        self.mandar_mensaje(parametro("AC_ENVIAR_SELECCION_USUARIO"), usuario)
