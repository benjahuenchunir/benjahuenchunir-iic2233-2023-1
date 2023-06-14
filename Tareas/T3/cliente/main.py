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

    host = data["host"]
    port = int(data["port"])

    back = backend.Logica(host, port)
    front = frontend.VentanaInicio()

    front.show()
    sys.exit(app.exec())
