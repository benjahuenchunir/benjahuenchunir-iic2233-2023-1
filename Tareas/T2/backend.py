from PyQt5.QtCore import QObject, QTimer, QPropertyAnimation, QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import random
import parametros as p
import os
import time

class Fantasma(QObject):
    identificador = 0

    def __init__(self, tipo, col, fil, senal_mover_fantasma, tiempo_movimiento, mapa) -> None:
        super().__init__()
        self.id = Fantasma.identificador
        Fantasma.identificador += 1
        self.tipo = tipo
        self.mapa = mapa
        self.x_original = col * p.TAMANO_GRILLA
        self.y_original = fil * p.TAMANO_GRILLA
        self.__col = col
        self.__fil = fil
        self.senal_mover = senal_mover_fantasma
        self.nombre_direccion = random.choice(p.NOMBRES_DIRECCIONES_FANTASMA[self.tipo])
        self.direccion = random.choice(p.DIRECCIONES_FANTASMA[self.nombre_direccion])
        self.timer_mover = QTimer(self)
        self.timer_mover.setInterval(tiempo_movimiento)
        self.timer_mover.timeout.connect(self.mover)

    @property
    def col(self):
        return self.__col

    @col.setter
    def col(self, nuevo_col):
        if not self.mapa[self.fil][nuevo_col] == p.MAPA_PARED:
            self.__col = max(1, min(nuevo_col, p.ANCHO_MAPA))

    @property
    def fil(self):
        return self.__fil

    @fil.setter
    def fil(self, nuevo_fil):
        if not self.mapa[nuevo_fil][self.col] == p.MAPA_PARED:
            self.__fil = max(1, min(nuevo_fil, p.LARGO_MAPA))

    def mover(self):
        col, fil = self.col, self.fil
        if self.tipo == p.TIPO_HORIZONTAL:
            self.col += self.direccion
        else:
            self.fil += self.direccion
        if self.col == col and self.fil == fil:
            if self.tipo != p.TIPO_VERTICAL:
                otra_direccion = p.NOMBRES_DIRECCIONES_FANTASMA[self.tipo].copy()
                otra_direccion.remove(self.nombre_direccion)
                self.nombre_direccion = otra_direccion[0]
            self.direccion = -self.direccion
            self.mover()
        else:
            self.senal_mover.emit(self.id, self.nombre_direccion, self.col * p.TAMANO_GRILLA, self.fil * p.TAMANO_GRILLA)


class Luigi(QObject):
    senal_animar_luigi = pyqtSignal(str, tuple)

    def __init__(self):
        super().__init__()
        self.vidas = p.CANTIDAD_VIDAS
        self.__x = 0
        self.__y = 0
        self.mapa = None

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, nuevo_x):
        col, fil = nuevo_x // p.TAMANO_GRILLA, self.y // p.TAMANO_GRILLA
        if not self.mapa[fil][col] == p.MAPA_PARED:
            self.__x = max(p.TAMANO_GRILLA, min(nuevo_x, p.TAMANO_GRILLA*p.ANCHO_MAPA))

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, nuevo_y):
        col, fil = self.x // p.TAMANO_GRILLA, nuevo_y // p.TAMANO_GRILLA
        if not self.mapa[fil][col] == p.MAPA_PARED:
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
    senal_iniciar_ventana_inicio = pyqtSignal(list)
    senal_nombre_invalido = pyqtSignal(str)
    senal_iniciar_constructor = pyqtSignal()
    senal_iniciar_juego = pyqtSignal()
    senal_iniciar_juego_constructor = pyqtSignal()

    senal_colocar_elemento = pyqtSignal(str, int, int)
    senal_actualizar_cantidad_elemento = pyqtSignal(str, str)

    senal_crear_luigi = pyqtSignal(int, int)
    senal_crear_fantasma = pyqtSignal(int, str, str, int, int)
    senal_crear_elemento = pyqtSignal(str, int, int)

    senal_actualizar_tiempo = pyqtSignal(str)
    senal_mover_fantasma = pyqtSignal(int, str, int, int)
    
    senal_reiniciar_fantasma  = pyqtSignal(int, int, int)

    senal_perder_vida = pyqtSignal(int)
    senal_limpiar_nivel = pyqtSignal()
    senal_pausar = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.fantasmas = []
        self.character = Luigi()
        self.ponderador_velocidad_fantasmas = random.uniform(p.MIN_VELOCIDAD, p.MAX_VELOCIDAD)
        self.tiempo_movimiento_fantasmas = int(1 / self.ponderador_velocidad_fantasmas)
        self.timer_colision_fantasmas = QTimer(self)
        self.timer_colision_fantasmas.setInterval(self.tiempo_movimiento_fantasmas)
        self.timer_colision_fantasmas.timeout.connect(self.verificar_colision)

        self.mapa = [[p.MAPA_VACIO for i in range(p.ANCHO_GRILLA)] for i in range(p.LARGO_GRILLA)]
        self.cantidad_elementos = p.MAXIMO_ELEMENTOS

        self.tiempo_restante = p.TIEMPO_CUENTA_REGRESIVA
        self.timer_juego = QTimer(self)
        self.timer_juego.setInterval(1000)
        self.timer_juego.timeout.connect(self.actualizar_tiempo)

        self.vidas = p.CANTIDAD_VIDAS
        self.pausa = False
        self.colision_fantasmas = True
        self.god_mode = False

    def colocar_elemento(self, elemento, x, y):
        col, fil = x // p.TAMANO_GRILLA, y // p.TAMANO_GRILLA
        if elemento and self.cantidad_elementos[elemento]:
            if col in (0, p.ANCHO_GRILLA - 1) or fil in (0, p.LARGO_GRILLA - 1) or self.mapa[fil][col] != p.MAPA_VACIO:
                return
            self.cantidad_elementos[elemento] -= 1
            self.mapa[fil][col] = elemento
            self.senal_actualizar_cantidad_elemento.emit(elemento, str(self.cantidad_elementos[elemento]))
            self.senal_colocar_elemento.emit(elemento, fil, col)

    def iniciar_ventana_inicio(self):
        mapas = []
        for mapa in os.listdir(p.PATH_MAPAS):
            with open(p.PATH_MAPAS + mapa, 'rt', encoding='utf-8') as f:
                mapas.append((mapa, f.readlines()))
        self.senal_iniciar_ventana_inicio.emit(mapas)

    def revisar_login(self, nombre_usuario, mapa):
        if len(nombre_usuario) == 0:
            self.senal_nombre_invalido.emit(p.NOMBRE_INVALIDO_VACIO)
        elif not nombre_usuario.isalnum():
            self.senal_nombre_invalido.emit(p.NOMBRE_INVALIDO_ALFANUMERICO)
        elif not p.MIN_CARACTERES <= len(nombre_usuario) <= p.MAX_CARACTERES:
            self.senal_nombre_invalido.emit(p.NOMBRE_INVALIDO_LARGO)
        elif mapa is not None:
            self.iniciar_juego(mapa)
        else:
            self.senal_iniciar_constructor.emit()

    def iniciar_juego(self, mapa):
        self.mapa = mapa
        self.leer_mapa(mapa)
        self.senal_actualizar_tiempo.emit(self.formatear_tiempo(self.tiempo_restante))
        self.timer_juego.start()
        self.senal_iniciar_juego.emit()

    def iniciar_juego_constructor(self):
        self.character.mapa = self.mapa
        self.leer_mapa(self.mapa)
        self.senal_actualizar_tiempo.emit(self.formatear_tiempo(self.tiempo_restante))
        self.timer_juego.start()
        self.senal_iniciar_juego_constructor.emit()

    def leer_mapa(self, filas):
        for fil, fila in enumerate(filas):
            for col, columna in enumerate(fila):
                if columna == p.MAPA_LUIGI:
                    self.character.x = col * p.TAMANO_GRILLA
                    self.character.y = fil * p.TAMANO_GRILLA
                    self.senal_crear_luigi.emit(self.character.x, self.character.y)
                elif columna in p.SPRITES_ENTIDADES:
                    self.crear_fantasma(columna, col, fil)
                elif columna in p.SPRITES_ELEMENTOS.keys():
                    self.senal_crear_elemento.emit(columna, col, fil)

    def crear_fantasma(self, tipo, col, fil):
        fantasma = Fantasma(p.FANTASMA_CONVERSION[tipo], col, fil, self.senal_mover_fantasma, self.tiempo_movimiento_fantasmas * 1000, self.mapa)
        fantasma.timer_mover.start()
        self.timer_colision_fantasmas.start()
        self.fantasmas.append(fantasma)
        self.senal_crear_fantasma.emit(fantasma.id, fantasma.tipo, fantasma.nombre_direccion, col * p.TAMANO_GRILLA, fil * p.TAMANO_GRILLA)

    def pausar(self):
        self.pausa = False if self.pausa else True
        if self.pausa:
            self.timer_juego.stop()
            for fantasma in self.fantasmas:
                fantasma.timer_mover.stop()
        else:
            if not self.god_mode:
                self.timer_juego.start()
            for fantasma in self.fantasmas:
                fantasma.timer_mover.start()
        self.senal_pausar.emit(self.pausa)
    
    def actualizar_tiempo(self):
        self.tiempo_restante -= 1
        self.senal_actualizar_tiempo.emit(self.formatear_tiempo(self.tiempo_restante))
        if self.tiempo_restante == 0:
            self.timer_juego.stop()
            print('Acabo juego')

    def formatear_tiempo(self, segundos):
        minutos, segundos = divmod(segundos, 60)
        return f"{minutos}:{segundos}"

    def mover_personaje(self, key):
        self.character.move_character(key)
        self.verificar_colision

    def verificar_colision(self):
        pos_personaje = (self.character.x // p.TAMANO_GRILLA, self.character.y // p.TAMANO_GRILLA)
        if self.colision_fantasmas:
            for fantasma in self.fantasmas:
                if (fantasma.col, fantasma.fil) == pos_personaje:
                    print('Colision')
                    self.perder_vida()
                    '''      
                    self.leer_mapa(self.mapa)
                    '''

    def perder_vida(self):
        self.vidas -= 1
        if self.vidas != 0:
            #self.senal_limpiar_nivel.emit()
            self.senal_perder_vida.emit(str(self.vidas))

            self.reiniciar_nivel()
        else:
            pass
            #self.leer_mapa(self.mapa)

    def reiniciar_nivel(self):
        for fantasma in self.fantasmas:
            fantasma.x = fantasma.x_original
            fantasma.y = fantasma.y_original
            self.senal_reiniciar_fantasma.emit(fantasma.id, fantasma.x, fantasma.y)

    def eliminar_villanos(self):
        self.colision_fantasmas = False
        for fantasma in self.fantasmas:
            fantasma.timer_mover.stop()

    def activar_godmode(self):
        self.god_mode = True
        self.timer_juego.stop()
