from PyQt5 import QtGui
import parametros as p
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QPropertyAnimation, QPoint
import sys


class VentanaInicio(QWidget):

    senal_iniciar_juego = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setGeometry(200, 100, 300, 300)

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
        self.btn_login.clicked.connect(self.login)
        self.setStyleSheet("background-image: 'sprites/Fondos/fondo_inicio.png'")

    def login(self):
        print(self.txt_username.text())
        self.senal_iniciar_juego.emit(self.txt_username.text())


class Fantasma():
    pass


class Elemento():
    pass


class Luigi(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = {
            p.LUIGI_QUIETO: ['sprites/Personajes/luigi_front.png'],
            'up': ['sprites/Personajes/luigi_up_1.png', 'sprites/Personajes/luigi_up_2.png', 'sprites/Personajes/luigi_up_3.png'],
            'down': ['sprites/Personajes/luigi_down_1.png', 'sprites/Personajes/luigi_down_2.png', 'sprites/Personajes/luigi_down_3.png'],
            'left': ['sprites/Personajes/luigi_left_1.png', 'sprites/Personajes/luigi_left_2.png', 'sprites/Personajes/luigi_left_3.png'],
            'right': ['sprites/Personajes/luigi_rigth_1.png', 'sprites/Personajes/luigi_rigth_2.png', 'sprites/Personajes/luigi_rigth_3.png']
        }
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(400)
        self.anim.finished.connect(self.parar_movimiento)
        self.timer = QTimer(self)
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_image)
        self.current_direction = p.LUIGI_QUIETO
        self.current_image = 0
        self.setPixmap(QPixmap(self.images[self.current_direction][self.current_image]))

    def move_character(self, end_pos):
        self.anim.setEndValue(QPoint(*end_pos))
        self.timer.start()
        self.anim.start()

    def update_image(self):
        self.current_image = (self.current_image + 1) % len(self.images[self.current_direction])
        self.setPixmap(QPixmap(self.images[self.current_direction][self.current_image]))

    def parar_movimiento(self):
        self.current_direction = p.LUIGI_QUIETO
        self.timer.stop()
        self.update_image()


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.character = Luigi(self)
        self.tamano_cuadricula = p.TAMANO_CUADRICULA
        self.showMaximized()
        self.keys_pressed = set()

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        current_pos = self.character.pos()
        key = event.key()
        if Qt.Key_W == key:
            self.character.current_direction = 'up'
            self.character.move_character((current_pos.x(), current_pos.y() - self.tamano_cuadricula))

        if Qt.Key_A == key:
            self.character.current_direction = 'left'
            self.character.move_character((current_pos.x() - self.tamano_cuadricula, current_pos.y()))

        if Qt.Key_S == key:
            self.character.current_direction = 'down'
            self.character.move_character((current_pos.x(), current_pos.y() + self.tamano_cuadricula))

        if Qt.Key_D == key:
            self.character.current_direction = 'right'
            self.character.move_character((current_pos.x() + self.tamano_cuadricula, current_pos.y()))


if __name__ == '__main__':
    app = QApplication([])
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())
