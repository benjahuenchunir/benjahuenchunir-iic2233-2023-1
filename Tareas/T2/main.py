from frontend import VentanaInicio, VentanaCompleta
from backend import Juego
from PyQt5.QtWidgets import QApplication
import sys
import parametros as p


class DCCazaFantasmas():
    def __init__(self):
        self.backend = Juego()
        self.ventana_inicio = VentanaInicio()
        self.ventana_juego = VentanaCompleta()
        
    def conectar_senales_mapa(self):
        self.ventana_juego.menu_constructor.btn_jugar.clicked.connect(self.ventana_juego.cargar_mapa)
        self.ventana_juego.senal_cargar_mapa.connect(self.backend.leer_mapa)
        self.backend.senal_crear_luigi.connect(self.ventana_juego.mapa_juego.crear_luigi)
        self.backend.senal_crear_fantasma.connect(self.ventana_juego.mapa_juego.crear_fantasma)
        self.backend.senal_crear_elemento.connect(self.ventana_juego.mapa_juego.crear_elemento)
        self.backend.senal_iniciar_juego.connect(self.ventana_juego.jugar)
        
    def conectar(self):
        self.conectar_senales_mapa()
        self.ventana_inicio.senal_iniciar_juego.connect(self.backend.iniciar_juego)
        self.ventana_juego.mapa_juego.senal_mover_personaje.connect(
            self.backend.mover_personaje)
        self.backend.character.senal_animar_luigi.connect(self.ventana_juego.mapa_juego.mover_luigi)
        self.backend.senal_mover_fantasma.connect(
            self.ventana_juego.mapa_juego.mover_fantasmas)

    def iniciar(self):
        print('Llegue aca')
        self.ventana_juego.show()
    
    def jugar(self):
        self.ventana_juego.jugar()


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
