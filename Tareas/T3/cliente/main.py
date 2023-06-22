import frontend.frontend as frontend
import backend.backend as backend
from PyQt5.QtWidgets import QApplication
import sys
from utils.utils import parametro


class DCCachos:
    def __init__(self):
        port = int(parametro("port")) if len(sys.argv) < 2 else int(sys.argv[1])
        host = parametro("host") if len(sys.argv) < 3 else int(sys.argv[2])
        self.back = backend.Logica(host, port)
        self.inicio = frontend.VentanaInicio()
        self.juego = frontend.VentanaJuego()
        self.conectar_senales_inicio()
        self.conectar_senales_juego()

    def iniciar(self):
        self.back.conectar_servidor()
        self.inicio.show()

    def conectar_senales_inicio(self):
        self.inicio.btn_comenzar.pressed.connect(self.back.empezar_partida)
        self.inicio.btn_salir.pressed.connect(
            self.back.test_manejar_mensaje2
        )  # TODO creo que no necesito conectarlo, solo que salga y el server sabra
        self.back.senal_agregar_usuario.connect(self.inicio.agregar_usuario)
        self.back.senal_servidor_cerrado.connect(self.inicio.servidor_cerrado)
        self.back.senal_eliminar_usuario.connect(self.inicio.eliminar_usuario)

    def conectar_senales_juego(self):
        self.back.senal_empezar_juego.connect(self.inicio.close)
        self.back.senal_empezar_juego.connect(self.juego.iniciar)
        self.back.senal_cambiar_dados.connect(self.juego.actualizar_dados)
        self.back.senal_cambiar_numero_mayor.connect(self.juego.actualizar_numero_mayor)
        self.back.senal_actualizar_turnos.connect(self.juego.actualizar_turnos)
        self.juego.btn_anunciar_valor.clicked.connect(self.juego.enviar_anunciar_valor)
        self.juego.senal_env_anunciar_valor.connect(self.back.enviar_anunciar_valor)
        self.juego.btn_pasar.clicked.connect(self.back.enviar_pasar)
        self.juego.btn_cambiar_dados.clicked.connect(self.back.enviar_cambiar_dados)
        self.juego.btn_usar_poder.clicked.connect(self.back.enviar_usar_poder)
        self.juego.btn_dudar.clicked.connect(self.back.enviar_dudar)
        self.juego.senal_keys_pressed.connect(self.back.manejar_key_pressed)
        self.back.senal_mostrar_dados.connect(self.juego.mostrar_dados)
        self.back.senal_cambiar_vida.connect(self.juego.cambiar_vida)
        self.back.senal_ocultar_dados.connect(self.juego.ocultar_dados)
        self.back.senal_perder.connect(self.juego.perder)
        self.back.senal_ganar.connect(self.juego.ganar)


if __name__ == "__main__":

    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    sys.__excepthook__ = hook
    app = QApplication(sys.argv)

    juego = DCCachos()
    juego.iniciar()

    sys.exit(app.exec())
