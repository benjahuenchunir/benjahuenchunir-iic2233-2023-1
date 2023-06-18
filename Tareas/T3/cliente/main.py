import frontend.frontend as frontend
import backend.backend as backend
from PyQt5.QtWidgets import QApplication
import sys
from utils.utils import parametro


if __name__ == "__main__":
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication(sys.argv)

    port = int(parametro("port")) if len(sys.argv) < 2 else int(sys.argv[1])
    host = parametro("host") if len(sys.argv) < 3 else int(sys.argv[2])
    back = backend.Logica(host, port)
    front = frontend.VentanaInicio()

    front.btn_comenzar.pressed.connect(back.test_manejar_mensaje)
    front.btn_salir.pressed.connect(back.test_manejar_mensaje2)
    back.senal_agregar_usuario.connect(front.agregar_usuario)

    back.conectar_servidor()

    front.show()
    sys.exit(app.exec())
