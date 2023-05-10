import typing
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
import sys


class VentanaInicio(QWidget):

    senal_iniciar_juego = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Definimos la geometría de la ventana.
        # Parámetros: (x_superior_izq, y_superior_izq, ancho, alto)
        self.setGeometry(200, 100, 300, 300)

        # Podemos dar nombre a la ventana (Opcional)
        self.setWindowTitle('loginWindow')
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.label_username = QLabel("Usuario", self)
        self.txt_username = QLineEdit("", self)
        self.dropdown_menu = QComboBox()
        self.dropdown_menu.addItem("Opción 1")
        self.btn_login = QPushButton("Login", self)
        hbox.addWidget(self.label_username)
        hbox.addWidget(self.txt_username)
        vbox.addLayout(hbox)
        vbox.addWidget(self.dropdown_menu)
        vbox.addWidget(self.btn_login)
        self.setLayout(vbox)
        self.setStyleSheet('background-image: ("sprites/Fondos/fondo_inicio.png")')
        self.btn_login.clicked.connect(self.login)

    def login(self):
        print(self.txt_username.text())
        self.senal_iniciar_juego.emit(self.txt_username.text())


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.imagen_personaje = QPixmap('sprites/Personajes/luigi_front.png')
        self.character = QLabel("", self)
        self.speed = 15
        self.character.setPixmap(self.imagen_personaje)
        self.showMaximized()
        
    def keyPressEvent(self, event) -> None:
        x = self.character.x()
        y = self.character.y()
        if event.key() == Qt.Key_W:
            self.imagen_personaje = QPixmap('sprites/Personajes/luigi_up_1.png')
            self.character.move(x, y - self.speed)
        elif event.key() == Qt.Key_S:
            self.imagen_personaje = QPixmap('sprites/Personajes/luigi_down_1.png')
            self.character.move(x, y + self.speed)
        elif event.key() == Qt.Key_D:
            self.character.move(x + self.speed, y)
        elif event.key() == Qt.Key_A:
            self.character.move(x - self.speed, y)
        self.character.setPixmap(self.imagen_personaje)


if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaInicio()
    ventana.show()
    sys.exit(app.exec())
