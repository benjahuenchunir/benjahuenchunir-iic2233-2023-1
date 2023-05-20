from frontend import VentanaInicio, VentanaCompleta
from backend import Juego
from PyQt5.QtWidgets import QApplication
import sys
import parametros as p
import os


class DCCazaFantasmas():
    def __init__(self):
        self.backend = Juego()
        self.ventana_inicio = VentanaInicio()
        self.ventana_juego = VentanaCompleta()
        self.conectar_señales_ventanta_inicio()
        self.conectar_senales_ventana_constructor()
        self.conectar_senales_ventana_juego()

    def conectar_señales_ventanta_inicio(self):
        self.backend.senal_iniciar_ventana_inicio.connect(self.ventana_inicio.cargar_mapas)
        self.ventana_inicio.senal_login.connect(self.backend.revisar_login)
        self.backend.senal_nombre_invalido.connect(self.ventana_inicio.alerta_nombre_invalido)
        self.backend.senal_iniciar_constructor.connect(self.ventana_inicio.close)
        self.backend.senal_iniciar_constructor.connect(self.ventana_juego.show)
        self.backend.senal_iniciar_juego.connect(self.ventana_inicio.close)
        self.backend.senal_iniciar_juego.connect(self.ventana_juego.show)
        self.backend.senal_iniciar_juego.connect(self.ventana_juego.jugar)

    def conectar_senales_ventana_constructor(self):
        self.ventana_juego.menu_constructor.btn_jugar.clicked.connect(self.ventana_juego.cargar_mapa_constructor)

    def conectar_senales_ventana_juego(self):
        self.backend.senal_actualizar_tiempo.connect(self.ventana_juego.menu_juego.actualizar_tiempo)

    def conectar_senales_mapa(self):
        self.ventana_juego.senal_cargar_mapa.connect(self.backend.leer_mapa)
        self.backend.senal_crear_luigi.connect(self.ventana_juego.mapa_juego.crear_luigi)
        self.backend.senal_crear_fantasma.connect(self.ventana_juego.mapa_juego.crear_fantasma)
        self.backend.senal_crear_elemento.connect(self.ventana_juego.mapa_juego.crear_elemento)

    def conectar(self):
        self.conectar_senales_mapa()
        self.ventana_juego.mapa_juego.senal_mover_personaje.connect(
            self.backend.mover_personaje)
        self.backend.character.senal_animar_luigi.connect(self.ventana_juego.mapa_juego.mover_luigi)
        self.backend.senal_mover_fantasma.connect(
            self.ventana_juego.mapa_juego.mover_fantasmas)
        self.backend.senal_limpiar_nivel.connect(self.ventana_juego.limpiar_nivel)

    def iniciar(self):
        self.backend.iniciar_ventana_inicio()
    
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
