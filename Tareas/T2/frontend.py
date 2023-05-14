from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QPalette
import parametros as p
from PyQt5.QtWidgets import QWidget, QApplication, QStackedLayout, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QComboBox
from PyQt5.QtCore import pyqtSignal, QTimer, QPropertyAnimation, QPoint, Qt
import sys
from collections import defaultdict
import os


class VentanaInicio(QWidget):

    senal_iniciar_juego = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        #self.setFixedSize(p.ANCHO_GRILLA*100, p.ANCHO_GRILLA*100)
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("sprites/Fondos/fondo_inicio.png"))
        self.background.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.background.setGeometry(0, 0, 1000, 800)
        self.background.setScaledContents(True)
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


class MapaJuego(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mapa = QGridLayout(self)
        self.setLayout(self.mapa)
        for fil in range(p.LARGO_GRILLA):
            for col in range(p.ANCHO_GRILLA):
                if fil == 0 or fil == p.LARGO_GRILLA - 1 or col == 0 or col == p.ANCHO_GRILLA - 1:
                    borde = QLabel(self)
                    borde.setPixmap(QPixmap(os.path.join(p.PATH_ELEMENTOS, p.SPRITES_ELEMENTOS[p.MAPA_BORDE])).scaled(p.TAMANO_GRILLA, p.TAMANO_GRILLA))
                    self.mapa.addWidget(borde, fil, col)
                else:
                    fondo = QLabel(self)
                    fondo.setStyleSheet(f"""
                            background-color: #2D2C2C;
                            border: 2px solid #242323;
                        """)
                    fondo.setFixedSize(p.TAMANO_GRILLA, p.TAMANO_GRILLA)
                    self.mapa.addWidget(fondo, fil, col)

class VentanaTest(QWidget):
    def __init__(self):
        super().__init__()
        self.mapa = MapaJuego()
        self.setLayout(self.mapa.mapa)
                    
        self.label_luigi = QLabel(self)
        self.label_luigi.setPixmap(QPixmap("sprites/Personajes/luigi_front.png"))
        self.show()
    
    def keyPressEvent(self, event) -> None:
        current_pos = self.label_luigi.pos()
        self.label_luigi.move(current_pos.x() + 60, current_pos.y())


class Fantasma(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imagenes = defaultdict(list)
        self.current_direction = p.LUIGI_QUIETO
        self.current_image = 0
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(400)
        self.anim.finished.connect(self.parar_movimiento)
        self.timer = QTimer(self)
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.animar_luigi)
        self.cargar_imagenes_luigi()
        self.setGeometry(0, 0, p.TAMANO_GRILLA, p.TAMANO_GRILLA)
        
    def cargar_imagenes_luigi(self):
        for image in os.listdir(p.PATH_PERSONAJES):
            if p.NOMBRE_LUIGI in image:
                self.imagenes[os.path.splitext(image)[0].split('_')[1]].append(QPixmap(os.path.join(p.PATH_PERSONAJES, image)).scaled(p.TAMANO_GRILLA, p.TAMANO_GRILLA, Qt.KeepAspectRatio))
        self.setPixmap(self.imagenes[self.current_direction][self.current_image])

    def mover(self, direccion, final_pos):
        self.current_direction = direccion
        self.anim.setEndValue(QPoint(*final_pos))
        self.timer.start()
        self.anim.start()

    def animar_luigi(self):
        self.current_image = (self.current_image + 1) % len(self.imagenes[self.current_direction])
        self.setPixmap(self.imagenes[self.current_direction][self.current_image])

    def parar_movimiento(self):
        self.current_direction = p.LUIGI_QUIETO
        self.timer.stop()
        self.animar_luigi()

class Luigi(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images_luigi = defaultdict(list)
        self.current_direction = p.LUIGI_QUIETO
        self.current_image = 0
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(400)
        self.anim.finished.connect(self.parar_movimiento)
        self.timer = QTimer(self)
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.animar_luigi)
        self.cargar_imagenes_luigi()
        self.setGeometry(0, 0, p.TAMANO_GRILLA, p.TAMANO_GRILLA)
        
    def cargar_imagenes_luigi(self):
        for image in os.listdir(p.PATH_PERSONAJES):
            if p.NOMBRE_LUIGI in image:
                self.images_luigi[os.path.splitext(image)[0].split('_')[1]].append(QPixmap(os.path.join(p.PATH_PERSONAJES, image)).scaled(p.TAMANO_GRILLA, p.TAMANO_GRILLA, Qt.KeepAspectRatio))
        self.setPixmap(self.images_luigi[self.current_direction][self.current_image])

    def mover(self, direccion, final_pos):
        self.current_direction = direccion
        self.anim.setEndValue(QPoint(*final_pos))
        self.timer.start()
        self.anim.start()

    def animar_luigi(self):
        self.current_image = (self.current_image + 1) % len(self.images_luigi[self.current_direction])
        self.setPixmap(self.images_luigi[self.current_direction][self.current_image])

    def parar_movimiento(self):
        self.current_direction = p.LUIGI_QUIETO
        self.timer.stop()
        self.animar_luigi()


class VentanaJuego(QWidget):
    senal_mover_personaje = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self.mapa = QGridLayout()
        self.mapa.setSpacing(0)
        self.mapa.setContentsMargins(0, 0, 0, 0)
        self.pos_player = (0, 0)
        self.setLayout(self.mapa)
        self.setFixedSize(p.ANCHO_GRILLA * p.TAMANO_GRILLA, p.LARGO_GRILLA * p.TAMANO_GRILLA)
        
        self.fantasmas = {}

    def iniciar(self, mapa, fantasmas):
        self.cargar_mapa(mapa)
        self.label_luigi = Luigi(self)
        print(list(map(lambda x: int(x*p.TAMANO_GRILLA), self.pos_player)))
        self.label_luigi.move(*list(map(lambda x: int(x*p.TAMANO_GRILLA), self.pos_player)))
        self.crear_fantasmas(fantasmas)
        self.show()
        
    def cargar_mapa(self, filas):
        for fil in range(p.LARGO_GRILLA):
            for col in range(p.ANCHO_GRILLA):
                if fil == 0 or fil == p.LARGO_GRILLA - 1 or col == 0 or col == p.ANCHO_GRILLA - 1:
                    borde = QLabel(self)
                    borde.setPixmap(QPixmap(os.path.join(p.PATH_ELEMENTOS, p.SPRITES_ELEMENTOS[p.MAPA_BORDE])).scaled(p.TAMANO_GRILLA, p.TAMANO_GRILLA))
                    self.mapa.addWidget(borde, fil, col)
                else:
                    fondo = QLabel(self)
                    fondo.setStyleSheet(f"""
                            background-color: #2D2C2C;
                            border: 2px solid #242323;
                        """)
                    fondo.setFixedSize(p.TAMANO_GRILLA, p.TAMANO_GRILLA)
                    self.mapa.addWidget(fondo, fil, col)
        for fil, fila in enumerate(filas, 1):
            for col, columna in enumerate(fila, 1):
                if columna == p.MAPA_LUIGI:
                    self.pos_player = (fil, col)
                    print(self.pos_player)
                elif columna in p.SPRITES_ELEMENTOS.keys():
                    elemento = QLabel(self)
                    elemento.setPixmap(QPixmap(os.path.join(p.PATH_ELEMENTOS, p.SPRITES_ELEMENTOS[columna])).scaled(p.TAMANO_GRILLA, p.TAMANO_GRILLA))
                    self.mapa.addWidget(elemento, fil, col)
                
    def crear_fantasmas(self, fantasmas):
        for fantasma in fantasmas:
            label_fantasma = QLabel(self)
            label_fantasma.setPixmap(QPixmap('sprites\Personajes\white_ghost_left_1.png'))
            label_fantasma.setGeometry(fantasma.x, fantasma.y, p.TAMANO_GRILLA, p.TAMANO_GRILLA)
            self.fantasmas[fantasma.id] = label_fantasma

    def mover_fantasmas(self, posiciones: dict):
        for id, posicion in posiciones.items():
            self.fantasmas[id].move(*posicion)

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        if self.label_luigi.current_direction == p.LUIGI_QUIETO:
            current_pos = self.label_luigi.pos()
            key = event.key()
            self.senal_mover_personaje.emit(key)

    def mover_luigi(self, direccion, pos_final):
        self.label_luigi.mover(direccion, pos_final)

if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaJuego()
    ventana.show()
    sys.exit(app.exec())
