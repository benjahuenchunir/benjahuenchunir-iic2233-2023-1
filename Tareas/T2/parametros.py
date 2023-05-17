ANCHO_GRILLA = 11 # NO EDITAR
LARGO_GRILLA = 16 # NO EDITAR

# Complete con los demás parámetros
TAMANO_GRILLA = 50
ANCHO_MAPA = ANCHO_GRILLA - 2
LARGO_MAPA = LARGO_GRILLA - 2
TIEMPO_JUEGO = 110

MIN_CARACTERES = 5
MAX_CARACTERES = 10

LUIGI_QUIETO = 'front'

PATH_FONDOS = 'sprites\Fondos'
PATH_ELEMENTOS = 'sprites/Elementos/'
PATH_ENTIDADES = 'sprites/Personajes/'

NOMBRE_LUIGI = 'luigi'
CANTIDAD_VIDAS = 3


# Fantasmas
MIN_VELOCIDAD = 0.3
MAX_VELOCIDAD = 0.8
TIPO_HORIZONTAL = 'white'
TIPO_VERTICAL = 'red'
DERECHA = 'rigth'
IZQUIERDA = 'left'
VERTICAL = 'vertical'
NOMBRES_DIRECCIONES_FANTASMA = {TIPO_HORIZONTAL: [DERECHA, IZQUIERDA], TIPO_VERTICAL: [VERTICAL]}
DIRECCIONES_FANTASMA = {DERECHA: [TAMANO_GRILLA], IZQUIERDA: [-TAMANO_GRILLA], VERTICAL: [TAMANO_GRILLA, -TAMANO_GRILLA]}
ARRIBA = 'arriba'
ABAJO = 'abajo'

# Constructor
MAPA_BORDE = 'B'
MAPA_LUIGI = 'L'
MAPA_PARED = 'P'
MAPA_FUEGO = 'F'
MAPA_FANTASMA_H = 'H'
MAPA_FANTASMA_V = 'V'
MAPA_ESTRELLA = 'S'
MAPA_ROCA = 'R'

SPRITES_ELEMENTOS = {MAPA_BORDE: PATH_ELEMENTOS + 'bordermap.png',
                     MAPA_FUEGO: PATH_ELEMENTOS + 'fire.png',
                     MAPA_ESTRELLA: PATH_ELEMENTOS + 'osstar.png',
                     MAPA_ROCA: PATH_ELEMENTOS + 'rock.png',
                     MAPA_PARED: PATH_ELEMENTOS + 'wall.png'}
SPRITES_ENTIDADES = {
    MAPA_LUIGI: PATH_ENTIDADES + 'luigi_front.png',
    MAPA_FANTASMA_H: PATH_ENTIDADES + 'white_ghost_rigth_1.png',
    MAPA_FANTASMA_V: PATH_ENTIDADES + 'red_ghost_vertical_1.png',
}
FILTRO_TODOS = 'Todos'
FILTROS = {FILTRO_TODOS: SPRITES_ENTIDADES | SPRITES_ELEMENTOS, 'Bloques': SPRITES_ELEMENTOS, 'Entidades': SPRITES_ENTIDADES}

MAXIMO_LUIGI = 1
MAXIMO_ESTRELLA = 1
MAXIMO_ELEMENTOS = {
    MAPA_LUIGI: 1,
    MAPA_PARED: 5,
    MAPA_FUEGO: 3,
    MAPA_FANTASMA_H: 3,
    MAPA_FANTASMA_V: 2,
    MAPA_ESTRELLA: 1,
    MAPA_ROCA: 2
}

MAXIMO_FANTASMAS_VERTICAL = 2 # TODO es necesario estos, los defini con otro nombre y en diccionario
MAXIMO_FANTASMAS_HORIZONTAL = 3

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QIcon, QFont, QKeySequence, QDrag, QMouseEvent
import parametros as p
from PyQt5.QtWidgets import QListWidgetItem, QGraphicsView, QGraphicsScene, QGraphicsObject, QGraphicsPixmapItem, QAbstractItemView, QWidget, QShortcut, QListWidget, QMainWindow, QApplication, QStackedLayout, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QComboBox
from PyQt5.QtCore import pyqtSignal, QTimer, QObject, QPropertyAnimation, QPoint, Qt, QSize, QByteArray, QDataStream, QIODevice, QMimeData
import sys
from collections import defaultdict
import os

class AnimatedPixmapItem(QGraphicsPixmapItem, QGraphicsObject):
    def __init__(self, pixmap):
        QGraphicsPixmapItem.__init__(self, pixmap)
        QGraphicsObject.__init__(self)


class MapaJuego(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.mapa = QGridLayout(self)
        self.elemento_seleccionado = None
        self.elementos_por_poner = p.MAXIMO_ELEMENTOS # TODO otra manera de manejar esto es con el label del list_wdget
        self.mapa.setSpacing(0)
        self.mapa.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mapa)
        for fil in range(p.LARGO_GRILLA):
            for col in range(p.ANCHO_GRILLA):
                if fil == 0 or fil == p.LARGO_GRILLA - 1 or col == 0 or col == p.ANCHO_GRILLA - 1:
                    borde = QLabel(self)
                    borde.setPixmap(QPixmap(p.SPRITES_ELEMENTOS[p.MAPA_BORDE]).scaled(p.TAMANO_GRILLA, p.TAMANO_GRILLA))
                    self.mapa.addWidget(borde, fil, col)
                else:
                    fondo = QLabel(self)
                    fondo.setStyleSheet(f"""
                            background-color: #2D2C2C;
                            border: 2px solid #242323;
                        """)
                    fondo.setFixedSize(p.TAMANO_GRILLA, p.TAMANO_GRILLA)
                    self.mapa.addWidget(fondo, fil, col)
                    
        self.label_luigi = QLabel(self)
        self.label_luigi.setPixmap(QPixmap('sprites/Personajes/luigi_front.png'))
        
               
if __name__ == "__main__":
    app = QApplication([])

    game_map = MapaJuego()
    game_map.show()

    app.exec_()
