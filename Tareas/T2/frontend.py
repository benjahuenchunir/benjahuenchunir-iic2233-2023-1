from PyQt5.QtGui import QPixmap
import parametros as p
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox
from PyQt5.QtCore import pyqtSignal, QTimer, QPropertyAnimation, QPoint
import sys
from collections import defaultdict
import os


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


class VentanaJuego(QWidget):
    senal_mover_personaje = pyqtSignal(int, int, int)

    def __init__(self) -> None:
        super().__init__()
        self.label_luigi = QLabel(self)
        self.images_luigi = defaultdict(list)
        self.current_direction = p.LUIGI_QUIETO
        self.current_image = 0
        self.anim = QPropertyAnimation(self.label_luigi, b"pos")
        self.anim.setDuration(400)
        self.anim.finished.connect(self.parar_movimiento)
        self.timer = QTimer(self)
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.animar_luigi)
        self.fantasmas = {}

        self.cargar_imagenes_luigi()

    def cargar_imagenes_luigi(self):
        for image in os.listdir(p.PATH_PERSONAJES):
            if p.NOMBRE_LUIGI in image:
                self.images_luigi[os.path.splitext(image)[0].split('_')[1]].append(QPixmap(os.path.join(p.PATH_PERSONAJES, image)))
        self.label_luigi.setPixmap(self.images_luigi[self.current_direction][self.current_image])

    def crear_fantasmas(self, fantasmas):
        for fantasma in fantasmas:
            label_fantasma = QLabel(self)
            label_fantasma.move(fantasma.x, fantasma.y)
            label_fantasma.setPixmap(QPixmap('sprites\Personajes\white_ghost_left_1.png'))
            self.fantasmas[fantasma.id] = label_fantasma

    def mover_fantasmas(self, posiciones: dict):
        for id, posicion in posiciones.items():
            self.fantasmas[id].move(*posicion)

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        if self.current_direction == p.LUIGI_QUIETO:
            current_pos = self.label_luigi.pos()
            key = event.key()
            self.senal_mover_personaje.emit(key, current_pos.x(), current_pos.y())

    def mover_luigi(self, direccion, final_pos):
        self.current_direction = direccion
        self.anim.setEndValue(QPoint(*final_pos))
        self.timer.start()
        self.anim.start()

    def animar_luigi(self):
        self.current_image = (self.current_image + 1) % len(self.images_luigi[self.current_direction])
        self.label_luigi.setPixmap(self.images_luigi[self.current_direction][self.current_image])

    def parar_movimiento(self):
        self.current_direction = p.LUIGI_QUIETO
        self.timer.stop()
        self.animar_luigi()


if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaJuego()
    ventana.show()
    sys.exit(app.exec())
