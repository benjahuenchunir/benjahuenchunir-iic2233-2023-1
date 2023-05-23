from PyQt5.QtCore import QObject, QTimer, Qt, pyqtSignal
import random
import parametros as p
import os
from copy import deepcopy


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
                self.mapa[fil][col] = p.MAPA_VACIO
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
            self.senal_mover_roca.emit(self.id, self.col * p.TAMANO_GRILLA, self.fil * p.TAMANO_GRILLA)
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
            if self.mover_roca((nuevo_col, self.fil), (2 * nuevo_col - self.col, self.fil)):
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
            if self.mover_roca((self.col, nuevo_fil), (self.col, 2 * nuevo_fil - self.fil)):
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
            self.mapa[fil][col] = p.MAPA_VACIO
            if self.mapa[self.fil][self.col] not in (p.MAPA_ESTRELLA, p.MAPA_FUEGO):
                self.mapa[self.fil][self.col] = p.MAPA_LUIGI
            self.senal_animar_luigi.emit(
                direccion, (self.col * p.TAMANO_GRILLA,
                            self.fil * p.TAMANO_GRILLA)
            )

    def mover_roca(self, posicion, nueva_posicion):
        for roca in self.rocas:
            if (roca.col, roca.fil) == posicion:
                return roca.mover(*nueva_posicion)


class Juego(QObject):
    senal_iniciar_ventana_inicio = pyqtSignal(list)
    senal_nombre_invalido = pyqtSignal(str)
    senal_iniciar_constructor = pyqtSignal()
    senal_iniciar_juego = pyqtSignal()
    senal_iniciar_juego_constructor = pyqtSignal()

    senal_colocar_elemento = pyqtSignal(str, int, int)
    senal_elemento_no_valido = pyqtSignal(str)
    senal_filtrar_elementos = pyqtSignal(list)
    senal_actualizar_cantidad_elemento = pyqtSignal(str, str)

    senal_crear_luigi = pyqtSignal(int, int)
    senal_crear_fantasma = pyqtSignal(int, str, str, int, int)
    senal_crear_roca = pyqtSignal(int, int, int)
    senal_crear_elemento = pyqtSignal(str, int, int)

    senal_actualizar_tiempo = pyqtSignal(str)
    senal_mover_fantasma = pyqtSignal(int, str, int, int)
    senal_morir = pyqtSignal(int)
    senal_eliminar_fantasma = pyqtSignal(int)
    senal_mover_roca = pyqtSignal(int, int, int)

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
        self.mapa_original = [
            [p.MAPA_VACIO for i in range(p.ANCHO_GRILLA)]
            for i in range(p.LARGO_GRILLA)
        ]
        self.mapa = deepcopy(self.mapa_original)
        self.cantidad_elementos = p.MAXIMO_ELEMENTOS.copy()

        self.tiempo_restante = p.TIEMPO_CUENTA_REGRESIVA
        self.timer_juego = QTimer(self)
        self.timer_juego.setInterval(1000)
        self.timer_juego.timeout.connect(self.actualizar_tiempo)

        self.vidas = p.CANTIDAD_VIDAS - 1
        self.pausa = True
        self.colision_fantasmas = True
        self.god_mode = False
        self.senal_verificar_colision.connect(self.verificar_colision)
        self.senal_morir.connect(self.eliminar_fantasma)
        self.colision_detectada = False

    def colocar_elemento(self, elemento, x, y):
        col, fil = x // p.TAMANO_GRILLA, y // p.TAMANO_GRILLA
        if elemento and self.cantidad_elementos[elemento]:
            if (
                col in (0, p.ANCHO_GRILLA - 1)
                or fil in (0, p.LARGO_GRILLA - 1)
                or self.mapa_original[fil][col] != p.MAPA_VACIO
            ):
                self.senal_elemento_no_valido.emit(p.POSICION_INVALIDA)
                return
            self.cantidad_elementos[elemento] -= 1
            self.mapa_original[fil][col] = elemento
            self.senal_actualizar_cantidad_elemento.emit(
                elemento, str(self.cantidad_elementos[elemento])
            )
            self.senal_colocar_elemento.emit(elemento, fil, col)
        else:
            self.senal_elemento_no_valido.emit(p.MAXIMO_SPRITES_ALCANZADO)

    def iniciar_ventana_inicio(self):
        mapas = []
        for mapa in os.listdir(p.PATH_MAPAS):
            with open(p.PATH_MAPAS + mapa, "rt", encoding="utf-8") as f:
                mapa_final = [[p.MAPA_VACIO for i in range(p.ANCHO_GRILLA)]]
                for fila in f.readlines():
                    fila = [p.MAPA_VACIO] + list(fila) + [p.MAPA_VACIO]
                    mapa_final.append(fila)
                mapa_final.append([p.MAPA_VACIO for i in range(p.ANCHO_GRILLA)])
                mapas.append((mapa, deepcopy(mapa_final)))
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
                self.filtrar_elementos_constructor(p.FILTRO_TODOS)

    def filtrar_elementos_constructor(self, filtro):
        filtrados = []
        for nombre_mapa, nombre_archivo in p.FILTROS[filtro].items():
            if p.MAPA_BORDE in p.FILTROS[filtro] and nombre_archivo == p.FILTROS[filtro][p.MAPA_BORDE]:
                continue
            filtrados.append((nombre_mapa, nombre_archivo, str(self.cantidad_elementos[nombre_mapa])))
        self.senal_filtrar_elementos.emit(filtrados)

    def limpiar_mapa(self, filtro):
        self.mapa_original = [
            [p.MAPA_VACIO for i in range(p.ANCHO_MAPA)]
            for i in range(p.LARGO_MAPA)
        ]
        self.cantidad_elementos = p.MAXIMO_ELEMENTOS.copy()
        self.filtrar_elementos_constructor(filtro)

    def iniciar_juego(self, mapa):
        self.mapa_original = mapa
        self.mapa = deepcopy(self.mapa_original)
        self.character.mapa = self.mapa
        self.leer_mapa(mapa)
        self.senal_actualizar_tiempo.emit(
            self.formatear_tiempo(self.tiempo_restante))
        self.pausar()
        self.senal_iniciar_juego.emit()

    def iniciar_juego_constructor(self):
        if self.verificar_condiciones_mapa():
            self.mapa = deepcopy(self.mapa_original)
            self.character.mapa = self.mapa
            self.leer_mapa(self.mapa)
            self.senal_actualizar_tiempo.emit(
                self.formatear_tiempo(self.tiempo_restante))
            self.pausar()
            self.senal_iniciar_juego_constructor.emit()

    def verificar_condiciones_mapa(self):
        return (len(p.REQUISITOS_MINIMOS_CONSTRUCTOR) ==
                len([col for fila in self.mapa_original for col in fila
                     if col in p.REQUISITOS_MINIMOS_CONSTRUCTOR]))

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
                elif columna == p.MAPA_ROCA:
                    self.crear_roca(col, fil)
                elif columna in p.SPRITES_ELEMENTOS.keys():
                    self.senal_crear_elemento.emit(columna, col, fil)

    def crear_fantasma(self, tipo, col, fil):
        fantasma = Fantasma(
            tipo,
            p.FANTASMA_CONVERSION[tipo],
            col,
            fil,
            self.senal_mover_fantasma,
            self.senal_morir,
            self.senal_verificar_colision,
            self.tiempo_movimiento_fantasmas * 1000,
            self.mapa,
        )
        self.fantasmas.append(fantasma)
        self.senal_crear_fantasma.emit(
            fantasma.id,
            fantasma.tipo,
            fantasma.nombre_direccion,
            col * p.TAMANO_GRILLA,
            fil * p.TAMANO_GRILLA,
        )

    def crear_roca(self, col, fil):
        roca = Roca(col, fil, self.mapa, self.senal_mover_roca)
        self.character.rocas.append(roca)
        self.senal_crear_roca.emit(roca.id, col * p.TAMANO_GRILLA, fil * p.TAMANO_GRILLA)

    def eliminar_fantasma(self, id):
        for fantasma in self.fantasmas:
            if fantasma.id == id:
                fantasma.timer_mover.stop()
                self.senal_eliminar_fantasma.emit(id)
                break

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
            self.perder()

    def formatear_tiempo(self, segundos):
        minutos, segundos = divmod(segundos, 60)
        return f"{minutos}:{segundos}"

    def mover_personaje(self, key):
        self.character.move_character(key)
        self.verificar_colision()

    def verificar_colision(self):
        pos_personaje = (self.character.col, self.character.fil)
        if self.mapa[pos_personaje[1]][pos_personaje[0]] == p.MAPA_FUEGO:
            self.colision_detectada = True
            self.perder_vida()
            return
        if self.colision_fantasmas:
            for fantasma in self.fantasmas:
                if (fantasma.col, fantasma.fil) == pos_personaje and not self.colision_detectada:
                    self.colision_detectada = True
                    self.perder_vida()
                    break

    def perder_vida(self):
        if not self.god_mode:
            self.vidas -= 1
            self.senal_perder_vida.emit(str(self.vidas))
        if self.vidas > 0:
            self.reiniciar_nivel()
        else:
            self.perder()
        self.colision_detectada = False

    def reiniciar_nivel(self):
        self.colision_fantasmas = True
        self.senal_limpiar_nivel.emit()
        for fantasma in self.fantasmas:
            fantasma.timer_mover.stop()
        self.fantasmas.clear()
        self.character.rocas.clear()
        self.mapa = deepcopy(self.mapa_original)
        self.character.mapa = self.mapa
        self.leer_mapa(self.mapa)
        for fantasma in self.fantasmas:
            fantasma.timer_mover.start()

    def reiniciar_juego(self):
        self.god_mode = False
        self.colision_fantasmas = True
        self.pausa = False
        self.tiempo_restante = p.TIEMPO_CUENTA_REGRESIVA
        self.vidas = p.CANTIDAD_VIDAS - 1
        self.senal_perder_vida.emit(str(self.vidas))
        self.reiniciar_nivel()
        self.timer_juego.start()

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
