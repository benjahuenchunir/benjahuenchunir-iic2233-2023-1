from PyQt5.QtCore import QObject, QTimer, Qt, pyqtSignal
import random
import parametros as p


class Fantasma(QObject):
    identificador = 0

    def __init__(
        self, tipo_mapa, tipo, col, fil, senal_mover_fantasma, senal_morir,
        senal_verificar_colision, tiempo_movimiento, mapa
    ) -> None:
        super().__init__()
        self.id = Fantasma.identificador
        Fantasma.identificador += 1
        self.tipo_mapa = tipo_mapa
        self.tipo = tipo
        self.mapa = mapa
        self.col0 = col
        self.fil0 = fil
        self.__col = col
        self.__fil = fil
        self.senal_mover = senal_mover_fantasma
        self.senal_morir = senal_morir
        self.senal_verificar_colision = senal_verificar_colision
        self.nombre_direccion = random.choice(
            p.NOMBRES_DIRECCIONES_FANTASMA[self.tipo])
        self.direccion = random.choice(
            p.DIRECCIONES_FANTASMA[self.nombre_direccion])
        self.timer_mover = QTimer(self)
        self.timer_mover.setInterval(tiempo_movimiento)
        self.timer_mover.timeout.connect(self.mover)

    @property
    def col(self):
        return self.__col

    @col.setter
    def col(self, nuevo_col):
        nuevo_col = max(1, min(nuevo_col, p.ANCHO_MAPA))
        if not self.mapa[self.fil][nuevo_col] in p.COLISION_FANTASMAS:
            self.__col = nuevo_col

    @property
    def fil(self):
        return self.__fil

    @fil.setter
    def fil(self, nuevo_fil):
        nuevo_fil = max(1, min(nuevo_fil, p.LARGO_MAPA))
        if not self.mapa[nuevo_fil][self.col] in p.COLISION_FANTASMAS:
            self.__fil = nuevo_fil

    def mover(self):
        col, fil = self.col, self.fil
        if self.tipo == p.TIPO_HORIZONTAL:
            self.col += self.direccion
        else:
            self.fil += self.direccion
        if self.col == col and self.fil == fil:
            if self.tipo != p.TIPO_VERTICAL:
                nueva_dir = p.NOMBRES_DIRECCIONES_FANTASMA[self.tipo].copy()
                nueva_dir.remove(self.nombre_direccion)
                self.nombre_direccion = nueva_dir[0]
            self.direccion = -self.direccion
            self.mover()
        else:
            self.senal_mover.emit(
                self.id,
                self.nombre_direccion,
                self.col * p.TAMANO_GRILLA,
                self.fil * p.TAMANO_GRILLA,
            )
            if self.mapa[self.fil][self.col] == p.MAPA_FUEGO:
                self.senal_morir.emit(self.id)
            else:
                if self.mapa[fil][col] != p.MAPA_ESTRELLA:
                    self.mapa[fil][col] = p.MAPA_VACIO
                if self.mapa[self.fil][self.col] != p.MAPA_ESTRELLA:
                    self.mapa[self.fil][self.col] = self.tipo_mapa
                self.senal_verificar_colision.emit()


class Roca:
    identificador = 0

    def __init__(self, col, fil, mapa, senal_mover):
        self.id = Roca.identificador
        Roca.identificador += 1
        self.__fil = fil
        self.__col = col
        self.mapa = mapa
        self.senal_mover_roca = senal_mover

    @property
    def col(self):
        return self.__col

    @col.setter
    def col(self, nuevo_col):
        nuevo_col = max(1, min(nuevo_col, p.ANCHO_MAPA))
        if self.mapa[self.fil][nuevo_col] == p.MAPA_VACIO:
            self.__col = nuevo_col

    @property
    def fil(self):
        return self.__fil

    @fil.setter
    def fil(self, nuevo_fil):
        nuevo_fil = max(1, min(nuevo_fil, p.LARGO_MAPA))
        if self.mapa[nuevo_fil][self.col] == p.MAPA_VACIO:
            self.__fil = nuevo_fil

    def mover(self, nuevo_col, nuevo_fil):
        col, fil = self.col, self.fil
        self.col, self.fil = nuevo_col, nuevo_fil
        if (col, fil) != (self.col, self.fil):
            self.mapa[fil][col] = p.MAPA_VACIO
            self.mapa[self.fil][self.col] = p.MAPA_ROCA
            self.senal_mover_roca.emit(
                self.id, self.col * p.TAMANO_GRILLA,
                self.fil * p.TAMANO_GRILLA)
            return True


class Luigi(QObject):
    senal_animar_luigi = pyqtSignal(str, tuple)

    def __init__(self):
        super().__init__()
        self.vidas = p.CANTIDAD_VIDAS
        self.col0 = 0
        self.fil0 = 0
        self.__col = 0
        self.__fil = 0
        self.mapa = None
        self.rocas = []

    @property
    def col(self):
        return self.__col

    @col.setter
    def col(self, nuevo_col):
        nuevo_col = max(1, min(nuevo_col, p.ANCHO_MAPA))
        if self.mapa[self.fil][nuevo_col] == p.MAPA_ROCA:
            if self.mover_roca((nuevo_col, self.fil),
                               (2 * nuevo_col - self.col, self.fil)):
                self.__col = nuevo_col
        elif not self.mapa[self.fil][nuevo_col] == p.MAPA_PARED:
            self.__col = nuevo_col

    @property
    def fil(self):
        return self.__fil

    @fil.setter
    def fil(self, nuevo_fil):
        nuevo_fil = max(1, min(nuevo_fil, p.LARGO_MAPA))
        if self.mapa[nuevo_fil][self.col] == p.MAPA_ROCA:
            if self.mover_roca((self.col, nuevo_fil),
                               (self.col, 2 * nuevo_fil - self.fil)):
                self.__fil = nuevo_fil
        elif not self.mapa[nuevo_fil][self.col] == p.MAPA_PARED:
            self.__fil = nuevo_fil

    def move_character(self, key):
        col, fil = self.col, self.fil
        if key == Qt.Key_W:
            direccion = p.ARRIBA
            self.fil -= 1

        if key == Qt.Key_A:
            direccion = p.IZQUIERDA
            self.col -= 1

        if key == Qt.Key_S:
            direccion = p.ABAJO
            self.fil += 1

        if key == Qt.Key_D:
            direccion = p.DERECHA
            self.col += 1

        if col != self.col or fil != self.fil:
            if self.mapa[fil][col] != p.MAPA_ESTRELLA:
                self.mapa[fil][col] = p.MAPA_VACIO
            if self.mapa[self.fil][self.col] not in (p.MAPA_ESTRELLA,
                                                     p.MAPA_FUEGO):
                self.mapa[self.fil][self.col] = p.MAPA_LUIGI
            self.senal_animar_luigi.emit(
                direccion, (self.col * p.TAMANO_GRILLA,
                            self.fil * p.TAMANO_GRILLA)
            )

    def mover_roca(self, posicion, nueva_posicion):
        for roca in self.rocas:
            if (roca.col, roca.fil) == posicion:
                return roca.mover(*nueva_posicion)
