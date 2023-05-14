from frontend import VentanaInicio, VentanaJuego
from backend import Juego
from PyQt5.QtWidgets import QApplication
import sys
import parametros as p


class DCCazaFantasmas():
    def __init__(self):
        self.backend = Juego()
        self.ventana_inicio = VentanaInicio()
        self.ventana_juego = VentanaJuego()

    def conectar(self):
        self.ventana_inicio.senal_iniciar_juego.connect(
            self.backend.iniciar_juego)
        self.ventana_juego.senal_mover_personaje.connect(
            self.backend.mover_personaje)
        self.backend.character.senal_animar_luigi.connect(
            self.ventana_juego.mover_luigi)
        self.backend.senal_mover_fantasmas.connect(
            self.ventana_juego.mover_fantasmas)

    def iniciar(self):
        self.backend.crear_fantasmas([(200, 200)])
        self.backend.iniciar()
        self.ventana_juego.iniciar(self.cargar_mapa(), self.backend.fantasmas)

    def cargar_mapa(self):
        with open('mapas/mapa enunciado.txt', 'rt', encoding='utf-8') as f:
            return f.readlines()


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
