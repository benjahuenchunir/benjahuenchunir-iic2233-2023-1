import frontend
import backend
from PyQt5.QtWidgets import QApplication
import sys
import json

if __name__ == "__main__":
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication(sys.argv)

    with open("parametros.json", "rt") as f:
        data = json.loads(f.read())

    port = int(data["port"]) if len(sys.argv) < 2 else int(sys.argv[1])
    host = data["host"] if len(sys.argv) < 3 else int(sys.argv[2])
    back = backend.Logica(host, port)
    front = frontend.VentanaInicio(data)

    front.btn_comenzar.pressed.connect(back.mandar_comando)
    front.btn_salir.pressed.connect(back.eliminar_usuario)
    back.senal_agregar_usuario.connect(front.agregar_usuario)
    
    back.conectar_servidor()

    front.show()
    sys.exit(app.exec())
