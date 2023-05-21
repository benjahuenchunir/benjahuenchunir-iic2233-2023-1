from PyQt5.QtCore import QObject, QTimer, Qt, pyqtSignal
import random
import parametros as p
import os


class Fantasma(QObject):
    identificador = 0

    def __init__(
        self, tipo, col, fil, senal_mover_fantasma, senal_verificar_colision,
        tiempo_movimiento, mapa
    ) -> None:
        super().__init__()
        self.id = Fantasma.identificador
        Fantasma.identificador += 1
        self.tipo = tipo
        self.mapa = mapa
        self.col0 = col
        self.fil0 = fil
        self.__col = col
        self.__fil = fil
        self.senal_mover = senal_mover_fantasma
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
            self.senal_verificar_colision.emit()


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
            self.senal_animar_luigi.emit(
                direccion, (self.col * p.TAMANO_GRILLA,
                            self.fil * p.TAMANO_GRILLA)
            )


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

    senal_verificar_colision = pyqtSignal()
    senal_perder_vida = pyqtSignal(str)
    senal_limpiar_nivel = pyqtSignal()
    senal_pausar = pyqtSignal(bool)

    senal_terminar_partida = pyqtSignal(str, str, str, float)

    def __init__(self):
        super().__init__()
        self.nombre_usuario = None
        self.fantasmas = []
        self.character = Luigi()
        self.ponderador_velocidad_fantasmas = random.uniform(
            p.MIN_VELOCIDAD, p.MAX_VELOCIDAD
        )
        self.tiempo_movimiento_fantasmas = (
            int(1 / self.ponderador_velocidad_fantasmas))

        self.mapa = [
            [p.MAPA_VACIO for i in range(p.ANCHO_GRILLA)]
            for i in range(p.LARGO_GRILLA)
        ]
        self.cantidad_elementos = p.MAXIMO_ELEMENTOS

        self.tiempo_restante = p.TIEMPO_CUENTA_REGRESIVA
        self.timer_juego = QTimer(self)
        self.timer_juego.setInterval(1000)
        self.timer_juego.timeout.connect(self.actualizar_tiempo)

        self.vidas = p.CANTIDAD_VIDAS - 1
        self.pausa = True
        self.colision_fantasmas = True
        self.god_mode = False
        self.senal_verificar_colision.connect(self.verificar_colision)
        self.colision_detectada = False

    def colocar_elemento(self, elemento, x, y):
        col, fil = x // p.TAMANO_GRILLA, y // p.TAMANO_GRILLA
        if elemento and self.cantidad_elementos[elemento]:
            if (
                col in (0, p.ANCHO_GRILLA - 1)
                or fil in (0, p.LARGO_GRILLA - 1)
                or self.mapa[fil][col] != p.MAPA_VACIO
            ):
                return
            self.cantidad_elementos[elemento] -= 1
            self.mapa[fil][col] = elemento
            self.senal_actualizar_cantidad_elemento.emit(
                elemento, str(self.cantidad_elementos[elemento])
            )
            self.senal_colocar_elemento.emit(elemento, fil, col)

    def iniciar_ventana_inicio(self):
        mapas = []
        for mapa in os.listdir(p.PATH_MAPAS):
            with open(p.PATH_MAPAS + mapa, "rt", encoding="utf-8") as f:
                mapas.append((mapa, f.readlines()))
        self.senal_iniciar_ventana_inicio.emit(mapas)

    def revisar_login(self, nombre_usuario, mapa):
        if len(nombre_usuario) == 0:
            self.senal_nombre_invalido.emit(p.NOMBRE_INVALIDO_VACIO)
        elif not nombre_usuario.isalnum():
            self.senal_nombre_invalido.emit(p.NOMBRE_INVALIDO_ALFANUMERICO)
        elif not p.MIN_CARACTERES <= len(nombre_usuario) <= p.MAX_CARACTERES:
            self.senal_nombre_invalido.emit(p.NOMBRE_INVALIDO_LARGO)
        else:
            self.nombre_usuario = nombre_usuario
            if mapa is not None:
                self.iniciar_juego(mapa)
            else:
                self.senal_iniciar_constructor.emit()

    def iniciar_juego(self, mapa):
        self.mapa = mapa
        self.character.mapa = self.mapa
        self.leer_mapa(mapa)
        self.senal_actualizar_tiempo.emit(
            self.formatear_tiempo(self.tiempo_restante))
        self.pausar()
        self.senal_iniciar_juego.emit()

    def iniciar_juego_constructor(self):
        self.character.mapa = self.mapa
        self.leer_mapa(self.mapa)
        self.senal_actualizar_tiempo.emit(
            self.formatear_tiempo(self.tiempo_restante))
        self.pausar()
        self.senal_iniciar_juego_constructor.emit()

    def leer_mapa(self, filas):
        for fil, fila in enumerate(filas):
            for col, columna in enumerate(fila):
                if columna == p.MAPA_LUIGI:
                    self.character.col, self.character.col0 = col, col
                    self.character.fil, self.character.fil0 = fil, fil
                    self.senal_crear_luigi.emit(
                        self.character.col * p.TAMANO_GRILLA,
                        self.character.fil * p.TAMANO_GRILLA,
                    )
                elif columna in p.SPRITES_ENTIDADES:
                    self.crear_fantasma(columna, col, fil)
                elif columna in p.SPRITES_ELEMENTOS.keys():
                    self.senal_crear_elemento.emit(columna, col, fil)

    def crear_fantasma(self, tipo, col, fil):
        fantasma = Fantasma(
            p.FANTASMA_CONVERSION[tipo],
            col,
            fil,
            self.senal_mover_fantasma,
            self.senal_verificar_colision,
            self.tiempo_movimiento_fantasmas * 1000,
            self.mapa,
        )
        #fantasma.timer_mover.start()
        #self.timer_colision_fantasmas.start()
        self.fantasmas.append(fantasma)
        self.senal_crear_fantasma.emit(
            fantasma.id,
            fantasma.tipo,
            fantasma.nombre_direccion,
            col * p.TAMANO_GRILLA,
            fil * p.TAMANO_GRILLA,
        )

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
        self.senal_actualizar_tiempo.emit(
            self.formatear_tiempo(self.tiempo_restante))
        if self.tiempo_restante == 0:
            self.pausar()
            self.perder()

    def formatear_tiempo(self, segundos):
        minutos, segundos = divmod(segundos, 60)
        return f"{minutos}:{segundos}"

    def mover_personaje(self, key):
        self.character.move_character(key)
        self.verificar_colision()

    def verificar_colision(self):
        pos_personaje = (self.character.col, self.character.fil)
        if self.colision_fantasmas:
            for fantasma in self.fantasmas:
                if (fantasma.col, fantasma.fil) == pos_personaje and not self.colision_detectada:
                    print(f"Colision con {fantasma.id}")
                    self.colision_detectada = True
                    self.perder_vida()
                    break

    def perder_vida(self):
        self.vidas -= 1
        self.senal_perder_vida.emit(str(self.vidas))
        if self.vidas != 0:
            self.reiniciar_nivel()
        else:
            self.perder()

    def reiniciar_nivel(self):
        self.senal_limpiar_nivel.emit()
        for fantasma in self.fantasmas:
            fantasma.timer_mover.stop()
        self.fantasmas.clear()
        self.leer_mapa(self.mapa)
        for fantasma in self.fantasmas:
            fantasma.timer_mover.start()
        self.colision_detectada = False

    def eliminar_villanos(self):
        self.colision_fantasmas = False
        for fantasma in self.fantasmas:
            fantasma.timer_mover.stop()

    def activar_godmode(self):
        self.god_mode = True
        self.timer_juego.stop()

    def perder(self):
        self.pausar()
        self.senal_terminar_partida.emit(
            p.DERROTA,
            p.PATH_SONIDO_DERROTA,
            self.nombre_usuario,
            self.calcular_puntaje(),
        )

    def liberar_aossa(self):
        if (self.mapa[self.character.fil][self.character.col] ==
                p.MAPA_ESTRELLA):
            self.pausar()
            self.senal_terminar_partida.emit(
                p.VICTORIA,
                p.PATH_SONIDO_VICTORIA,
                self.nombre_usuario,
                self.calcular_puntaje(),
            )

    def calcular_puntaje(self):
        return (self.tiempo_restante * p.MULTIPLICADOR_PUNTAJE) / (
            p.CANTIDAD_VIDAS - self.vidas
        )
