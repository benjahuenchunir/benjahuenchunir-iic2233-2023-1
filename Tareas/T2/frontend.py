import typing
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QPropertyAnimation
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


class Character(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = {
            'front': ['sprites/Personajes/luigi_front.png'],
            'up': ['sprites/Personajes/luigi_up_1.png', 'sprites/Personajes/luigi_up_2.png', 'sprites/Personajes/luigi_up_3.png'],
            'down': ['sprites/Personajes/luigi_down_1.png', 'sprites/Personajes/luigi_down_2.png', 'sprites/Personajes/luigi_down_3.png'],
            'left': ['sprites/Personajes/luigi_left_1.png', 'sprites/Personajes/luigi_left_2.png', 'sprites/Personajes/luigi_left_3.png'],
            'right': ['sprites/Personajes/luigi_rigth_1.png', 'sprites/Personajes/luigi_rigth_2.png', 'sprites/Personajes/luigi_rigth_3.png']
        }
        self.current_direction = 'front'
        self.current_image = 0
        self.setPixmap(QPixmap(self.images[self.current_direction][self.current_image]))

    def update_image(self):
        self.current_image = (self.current_image_index + 1) % len(self.images[self.current_direction])
        self.setPixmap(QPixmap(self.images[self.current_direction][self.current_image]))


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.character = Character(self)
        self.speed = 5
        self.showMaximized()
        self.keys_pressed = set()

        self.movement_timer = QTimer(self)
        self.movement_timer.timeout.connect(self.move_character)
        self.movement_timer.start(25)

    def keyPressEvent(self, event):
        key = event.key()
        print(key)
        self.keys_pressed.add(key)

    def keyReleaseEvent(self, event):
        key = event.key()
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def move_character(self):
        current_pos = self.character.pos()

        if Qt.Key_W in self.keys_pressed:
            self.character.current_direction = 'up'
            self.character.move(current_pos.x(), current_pos.y() - self.speed)

        if Qt.Key_A in self.keys_pressed:
            self.character.current_direction = 'left'
            self.character.move(current_pos.x() - self.speed, current_pos.y())

        if Qt.Key_S in self.keys_pressed:
            self.character.current_direction = 'down'
            self.character.move(current_pos.x(), current_pos.y() + self.speed)

        if Qt.Key_D in self.keys_pressed:
            self.character.current_direction = 'right'
            self.character.move(current_pos.x() + self.speed, current_pos.y())

        if len(self.keys_pressed) == 0:
            self.character.current_direction = 'front'

        self.character.update_image()


if __name__ == '__main__':
    app = QApplication([])
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())
