from PyQt5.QtCore import QObject, QTimer, QPropertyAnimation, QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import random
import parametros as p
import os


class Fantasma():
    identificador = 0
    
    def __init__(self, tipo, x, y) -> None:
        self.id = Fantasma.identificador
        Fantasma.identificador += 1
        self.x = x
        self.y = y
        self.direccion = random.choice(p.DIRECCIONES_FANTASMA)
        self.tipo = tipo

    def mover(self):  # TODO verificar que no se salga
        if self.tipo == p.TIPO_HORIZONTAL:
            self.x += self.direccion
        else:
            self.y += self.direccion
        return {self.id: (self.x, self.y)}


class Elemento():
    pass


class Luigi(QObject):
    senal_animar_luigi = pyqtSignal(str, tuple)

    def __init__(self):
        super().__init__()
        self.vidas = p.CANTIDAD_VIDAS

    def move_character(self, key, x, y):
        if key == Qt.Key_W:
            direccion = 'up'
            final_pos = (x, y - p.TAMANO_GRILLA)

        if key == Qt.Key_A:
            direccion = 'left'
            final_pos = (x - p.TAMANO_GRILLA, y)

        if key == Qt.Key_S:
            direccion = 'down'
            final_pos = (x, y + p.TAMANO_GRILLA)

        if key == Qt.Key_D:
            direccion = 'rigth'
            final_pos = (x + p.TAMANO_GRILLA, y)

        self.senal_animar_luigi.emit(direccion, final_pos)


class Juego(QObject):
    senal_mover_fantasmas = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.character = Luigi()
        self.fantasmas = []
        self.ponderador_velocidad_fantasmas = random.uniform(p.MIN_VELOCIDAD, p.MAX_VELOCIDAD)
        self.tiempo_movimiento_fantasmas = int(1 / self.ponderador_velocidad_fantasmas)
        self.timer_mov_fantasmas = QTimer(self)
        print(self.tiempo_movimiento_fantasmas)
        self.timer_mov_fantasmas.setInterval(self.tiempo_movimiento_fantasmas * 1000)
        self.timer_mov_fantasmas.timeout.connect(self.mover_fantasmas)

    def iniciar(self):
        self.timer_mov_fantasmas.start()

    def crear_fantasmas(self, posiciones):
        for posicion in posiciones:
            fantasma = Fantasma(random.choice([p.TIPO_HORIZONTAL, p.TIPO_VERTICAL]), *posicion)
            self.fantasmas.append(fantasma)

    def mover_fantasmas(self):
        movimientos = {}
        for fantasma in self.fantasmas:
            movimientos.update(fantasma.mover())
        self.senal_mover_fantasmas.emit(movimientos)

    def mover_personaje(self, key, x, y):
        self.character.move_character(key, x, y)

    def iniciar_juego(self, nombre_usuario: str):
        print("entre")
        if nombre_usuario.isalpha() and len(nombre_usuario):
            return True