from PyQt5.QtCore import QObject


class Juego(QObject):
    def __init__(self):
        super().__init__()
        self.usuartio = None

    def iniciar_juego(self, nombre_usuario: str):
        print("entre")
        if nombre_usuario.isalpha() and len(nombre_usuario):
            return True