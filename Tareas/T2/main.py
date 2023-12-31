from frontend import VentanaInicio, VentanaCompleta
from backend import Juego
from PyQt5.QtWidgets import QApplication
import sys


class DCCazaFantasmas:
    def __init__(self):
        self.backend = Juego()
        self.ventana_inicio = VentanaInicio()
        self.ventana_juego = VentanaCompleta()
        self.conectar_señales_ventanta_inicio()
        self.conectar_senales_ventana_constructor()
        self.conectar_senales_ventana_juego()

    def conectar_señales_ventanta_inicio(self):
        self.ventana_inicio.btn_login.clicked.connect(
            self.ventana_inicio.login)
        self.ventana_inicio.btn_exit.clicked.connect(self.ventana_inicio.close)
        self.backend.senal_iniciar_ventana_inicio.connect(
            self.ventana_inicio.cargar_mapas
        )
        self.ventana_inicio.senal_login.connect(self.backend.revisar_login)
        self.backend.senal_nombre_invalido.connect(
            self.ventana_inicio.alerta_nombre_invalido
        )
        self.backend.senal_iniciar_constructor.connect(
            self.ventana_inicio.close
            )
        self.backend.senal_iniciar_constructor.connect(self.ventana_juego.show)
        self.backend.senal_iniciar_juego.connect(self.ventana_inicio.close)
        self.backend.senal_iniciar_juego.connect(self.ventana_juego.show)
        self.backend.senal_iniciar_juego.connect(self.ventana_juego.jugar)

    def conectar_senales_ventana_constructor(self):
        (self.ventana_juego.menu_constructor.
         filtro_elementos.currentTextChanged.connect(
             self.backend.filtrar_elementos_constructor))
        self.backend.senal_filtrar_elementos.connect(
            self.ventana_juego.menu_constructor.filtrar_lista)
        self.ventana_juego.menu_constructor.btn_limpiar.clicked.connect(
            self.ventana_juego.mapa.limpiar_mapa)
        self.ventana_juego.menu_constructor.btn_limpiar.clicked.connect(
            self.ventana_juego.menu_constructor.limpiar_mapa
        )
        self.ventana_juego.menu_constructor.senal_limpiar_mapa.connect(
            self.backend.limpiar_mapa)
        self.ventana_juego.menu_constructor.btn_jugar.clicked.connect(
            self.backend.iniciar_juego_constructor
        )
        self.backend.senal_iniciar_juego_constructor.connect(
            self.ventana_juego.jugar
            )
        self.ventana_juego.mapa.senal_on_click.connect(
            self.ventana_juego.emitir_colocar_elemento
        )
        self.backend.senal_elemento_no_valido.connect(
            self.ventana_juego.mostrar_alerta
        )
        self.ventana_juego.senal_colocar_elemento_constructor.connect(
            self.backend.colocar_elemento
        )
        self.backend.senal_colocar_elemento.connect(
            self.ventana_juego.mapa.colocar_elemento
        )
        self.backend.senal_actualizar_cantidad_elemento.connect(
            self.ventana_juego.menu_constructor.actualizar_cantidad_elemento
        )

    def conectar_senales_ventana_juego(self):
        self.ventana_juego.senal_cargar_mapa.connect(self.backend.leer_mapa)
        self.backend.senal_crear_luigi.connect(
            self.ventana_juego.mapa_juego.crear_luigi
        )
        self.backend.senal_crear_fantasma.connect(
            self.ventana_juego.mapa_juego.crear_fantasma
        )
        self.backend.senal_crear_roca.connect(
            self.ventana_juego.mapa_juego.crear_roca
        )
        self.backend.senal_crear_elemento.connect(
            self.ventana_juego.mapa_juego.crear_elemento
        )
        self.backend.senal_actualizar_tiempo.connect(
            self.ventana_juego.menu_juego.actualizar_tiempo
        )
        self.ventana_juego.mapa_juego.senal_mover_personaje.connect(
            self.backend.mover_personaje
        )
        self.backend.character.senal_animar_luigi.connect(
            self.ventana_juego.mapa_juego.mover_luigi
        )
        self.backend.senal_mover_fantasma.connect(
            self.ventana_juego.mapa_juego.mover_fantasmas
        )
        self.backend.senal_mover_roca.connect(
            self.ventana_juego.mapa_juego.mover_roca)
        self.backend.senal_perder_vida.connect(
            self.ventana_juego.menu_juego.actualizar_vidas
        )
        self.backend.senal_limpiar_nivel.connect(
            self.ventana_juego.mapa_juego.limpiar_nivel
        )
        self.ventana_juego.menu_juego.btn_pausar.clicked.connect(
            self.backend.pausar
            )
        self.ventana_juego.senal_pausar.connect(self.backend.pausar)
        self.backend.senal_pausar.connect(self.ventana_juego.pausar)

        self.ventana_juego.mapa_juego.senal_eliminar_villanos.connect(
            self.backend.eliminar_villanos
        )
        self.ventana_juego.mapa_juego.senal_godmode.connect(
            self.backend.activar_godmode
        )
        self.ventana_juego.mapa_juego.senal_liberar_aossa.connect(
            self.backend.liberar_aossa
        )

        self.backend.senal_terminar_partida.connect(
            self.ventana_juego.terminar_partida
        )
        self.backend.senal_eliminar_fantasma.connect(
            self.ventana_juego.mapa_juego.eliminar_fantasma)
        self.ventana_juego.senal_reiniciar_juego.connect(
            self.backend.reiniciar_juego)

    def iniciar(self):
        self.backend.iniciar_ventana_inicio()


if __name__ == "__main__":

    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    sys.__excepthook__ = hook

    app = QApplication([])
    game = DCCazaFantasmas()
    game.iniciar()

    sys.exit(app.exec())
