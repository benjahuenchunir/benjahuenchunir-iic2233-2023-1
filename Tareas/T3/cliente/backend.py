import socket
from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread


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
            listening_server_thread = Thread(
                    target=self.escuchar_servidor,
                    daemon=True)
            listening_server_thread.start()
        except ConnectionError:
            print('Conexion terminada')
            self.socket_cliente.close()
            exit()

    def escuchar_servidor(self):
        data = self.socket_cliente.recv(4096).decode('utf-8')
        if 'agregar' in data:
            id = data.split(':')[-1]
            print(id)
            self.senal_agregar_usuario.emit(id)
            print("señal emitida")
        else:
            print("la data era otra")

    def mandar_comando(self) -> None:
        comando = "comenzar"
        self.socket_cliente.send(comando.encode("utf-8"))

    def eliminar_usuario(self) -> None:
        comando = "salir"
        self.socket_cliente.send(comando.encode("utf-8"))
