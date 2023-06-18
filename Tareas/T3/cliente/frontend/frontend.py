from PyQt5.QtGui import QPixmap, QMouseEvent, QFont
from PyQt5.QtWidgets import (
    QListWidgetItem,
    QMessageBox,
    QAbstractItemView,
    QStackedWidget,
    QWidget,
    QListWidget,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QApplication,
    QMainWindow,
    QSizePolicy,
)
from PyQt5.QtCore import QUrl, pyqtSignal, Qt, QSize
from PyQt5.QtMultimedia import QSoundEffect
import sys
import json
from parametros import parametro


class VentanaInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana inicio")
        self.move(0, 0)
        self.setFixedSize(
            parametro("ventana_inicio_size"),
            parametro("ventana_inicio_size"),
        )

        main_layout = QVBoxLayout()
        background = QLabel(self)
        background.setPixmap(
            QPixmap(parametro("path_fondo_inicio")).scaled(
                self.width(), self.height()
            )
        )
        background.setGeometry(0, 0, self.width(), self.height())
        label_sala_espera = QLabel("SALA DE ESPERA", self)
        label_sala_espera.setAlignment(Qt.AlignHCenter)  # type: ignore
        label_sala_espera.setFont(QFont("Arial", 30, weight=QFont.Bold))
        main_layout.addWidget(label_sala_espera)
        self.players_layout = QHBoxLayout()
        main_layout.addLayout(self.players_layout)
        self.btn_comenzar = QPushButton("Comenzar", self)
        self.btn_salir = QPushButton("Salir", self)
        main_layout.addWidget(self.btn_comenzar)
        main_layout.addWidget(self.btn_salir)
        self.setLayout(main_layout)
        self.usuarios = {}

    def mostrar_alerta(self, mensaje):
        alerta = QMessageBox(self)
        alerta.setWindowTitle("Alerta")
        alerta.setIcon(QMessageBox.Warning)
        alerta.setText(mensaje)
        alerta.setStandardButtons(QMessageBox.Ok)
        alerta.exec()

    def agregar_usuario(self, id):
        print("Agregando label usuario")
        label_usuario = QLabel(self)
        label_usuario.setPixmap(QPixmap("Sprites/extra/user_profile.png"))
        self.usuarios[id] = label_usuario
        self.players_layout.addWidget(label_usuario)


if __name__ == "__main__":

    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    sys.__excepthook__ = hook

    app = QApplication([])
    game = VentanaInicio()
    game.show()

    sys.exit(app.exec())
