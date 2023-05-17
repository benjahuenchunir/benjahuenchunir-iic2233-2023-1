from PyQt5.QtCore import QObject, QTimer, QPropertyAnimation, QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import random
import parametros as p
import os


class Fantasma(QObject):
    identificador = 0

    def __init__(self, tipo, x, y, senal_mover_fantasma, tiempo_movimiento) -> None:
        super().__init__()
        self.id = Fantasma.identificador
        Fantasma.identificador += 1
        self.tipo = tipo
        self.__x = x
        self.__y = y
        self.senal_mover = senal_mover_fantasma
        print(self.tipo)
        self.nombre_direccion = random.choice(p.NOMBRES_DIRECCIONES_FANTASMA[self.tipo])
        self.direccion = random.choice(p.DIRECCIONES_FANTASMA[self.nombre_direccion])
        self.timer_mover = QTimer(self)
        self.timer_mover.setInterval(tiempo_movimiento)
        self.timer_mover.timeout.connect(self.mover)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, nuevo_x):
        self.__x = max(p.TAMANO_GRILLA, min(nuevo_x, p.TAMANO_GRILLA*p.ANCHO_MAPA))

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, nuevo_y):
        self.__y = max(p.TAMANO_GRILLA, min(nuevo_y, p.TAMANO_GRILLA*p.LARGO_MAPA))

    def mover(self):
        x, y = self.x, self.y
        if self.tipo == p.TIPO_HORIZONTAL:
            self.x += self.direccion
        else:
            self.y += self.direccion
        if self.x == x and self.y == y:
            if self.tipo != p.TIPO_VERTICAL:
                otra_direccion = p.NOMBRES_DIRECCIONES_FANTASMA[self.tipo].copy()
                otra_direccion.remove(self.nombre_direccion)
                self.nombre_direccion = otra_direccion[0]
            self.direccion = -self.direccion
        else:
            self.senal_mover.emit(self.id, self.nombre_direccion, self.x, self.y)


class Luigi(QObject):
    senal_animar_luigi = pyqtSignal(str, tuple)

    def __init__(self):
        super().__init__()
        self.vidas = p.CANTIDAD_VIDAS
        self.__x = 0
        self.__y = 0

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, nuevo_x):
        self.__x = max(p.TAMANO_GRILLA, min(nuevo_x, p.TAMANO_GRILLA*p.ANCHO_MAPA))

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, nuevo_y):
        self.__y = max(p.TAMANO_GRILLA, min(nuevo_y, p.TAMANO_GRILLA*p.LARGO_MAPA))

    def move_character(self, key):
        x, y = self.x, self.y
        if key == Qt.Key_W:
            direccion = 'up'
            self.y -= p.TAMANO_GRILLA

        if key == Qt.Key_A:
            direccion = 'left'
            self.x -= p.TAMANO_GRILLA

        if key == Qt.Key_S:
            direccion = 'down'
            self.y += p.TAMANO_GRILLA

        if key == Qt.Key_D:
            direccion = 'rigth'
            self.x += p.TAMANO_GRILLA

        if x != self.x or y != self.y:
            self.senal_animar_luigi.emit(direccion, (self.x, self.y))


class Juego(QObject):
    senal_mover_fantasma = pyqtSignal(int, str, int, int)
    senal_crear_luigi = pyqtSignal(int, int)
    senal_crear_fantasma = pyqtSignal(int, str, str, int, int)
    senal_crear_elemento = pyqtSignal(str, int, int)
    senal_iniciar_juego = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.fantasmas = []
        self.character = Luigi()
        self.ponderador_velocidad_fantasmas = random.uniform(p.MIN_VELOCIDAD, p.MAX_VELOCIDAD)
        self.tiempo_movimiento_fantasmas = int(1 / self.ponderador_velocidad_fantasmas)
        
    def cargar_mapa(self):
        with open('mapas/mapa enunciado.txt', 'rt', encoding='utf-8') as f:
            return f.readlines()

    def leer_mapa(self, filas):
        for fil, fila in enumerate(filas):
            for col, columna in enumerate(fila):
                if columna == p.MAPA_LUIGI:
                    self.character.x = col * p.TAMANO_GRILLA
                    self.character.y = fil * p.TAMANO_GRILLA
                    self.senal_crear_luigi.emit(self.character.x, self.character.y)
                elif columna in p.SPRITES_ENTIDADES:
                    self.crear_fantasma(columna, col * p.TAMANO_GRILLA, fil * p.TAMANO_GRILLA)
                elif columna in p.SPRITES_ELEMENTOS.keys():
                    self.senal_crear_elemento.emit(columna, col, fil)
        self.senal_iniciar_juego.emit()

    def crear_fantasma(self, tipo, x, y):
        fantasma = Fantasma(p.FANTASMA_CONVERSION[tipo], x, y, self.senal_mover_fantasma, self.tiempo_movimiento_fantasmas * 1000)
        fantasma.timer_mover.start()
        self.fantasmas.append(fantasma)
        self.senal_crear_fantasma.emit(fantasma.id, fantasma.tipo, fantasma.nombre_direccion, x, y)

    def mover_personaje(self, key):
        self.character.move_character(key)

    def iniciar_juego(self, nombre_usuario: str):
        print("entre")
        if nombre_usuario.isalpha() and len(nombre_usuario):
            return True