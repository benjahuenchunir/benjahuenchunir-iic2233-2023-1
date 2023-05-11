from frontend import VentanaInicio
from backend import Juego
from PyQt5.QtWidgets import QApplication
import sys


class DCCazaFantasmas():
    def __init__(self):
        self.ventana_inicio = VentanaInicio()
        self.backend = Juego()

    def conectar(self):
        self.ventana_inicio.senal_iniciar_juego.connect(
            self.backend.iniciar_juego)

    def iniciar(self):
        self.ventana_inicio.show()

    def cargar_mapa(self):
        with open('mapas/fantasma muere.txt', 'rt', encoding='utf-8') as f:
            for linea in f.readlines():
                pass


if __name__ == '__main__':
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    sys.__excepthook__ = hook

    app = QApplication([])
    game = DCCazaFantasmas()
    game.conectar()
    game.iniciar()

    sys.exit(app.exec())
