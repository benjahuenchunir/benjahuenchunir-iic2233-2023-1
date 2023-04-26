import random
import entidades_torneo as entidades
import parametros
import os
from collections import defaultdict


class Torneo:
    def __init__(self, arena, equipo, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.arena = arena
        self.equipo = equipo
        self.eventos = [parametros.LLUVIA, parametros.TERREMOTO,
                        parametros.DERRUMBE]
        self.mochila = []
        self.__metros_cavados = 0
        self.meta = parametros.METROS_META
        self.dias_transcurridos = 1
        self.dias_totales = parametros.DIAS_TOTALES_TORNEO

    @property
    def metros_cavados(self):
        return self.__metros_cavados

    @metros_cavados.setter
    def metros_cavados(self, value):
        self.__metros_cavados = round(max(0, value), 2)

    def simular_dia(self):
        """
        Simula un dia del DCCavaCava
        """
        print(f"\n{f'Día {self.dias_transcurridos}':^53s}")
        print("-"*53)
        trabajadores = [excavador for excavador in self.equipo
                        if not excavador.descansando]
        descansando = [excavador for excavador in self.equipo
                       if excavador.descansando]
        self.cavar(trabajadores)
        self.encontrar_items(trabajadores)
        self.iniciar_evento()
        self.editar_energia(trabajadores, descansando)
        self.dias_transcurridos += 1
        if self.dias_transcurridos <= self.dias_totales:
            return True

    def cavar(self, trabajadores) -> None:
        """
        Manda a los trabajadores a cavar
        """
        print(f"Metros Cavados: {self.metros_cavados}")
        metros_cavados_dia = 0
        for excavador in trabajadores:
            nuevos_metros_cavados = excavador.cavar(self.arena.dificultad)
            metros_cavados_dia += nuevos_metros_cavados
            self.metros_cavados += nuevos_metros_cavados
            print(f"{excavador.nombre} ha cavado"
                  f" {nuevos_metros_cavados} metros.")
        print(f"El equipo ha cavado {metros_cavados_dia} metros.")

    def encontrar_items(self, trabajadores) -> None:
        """
        Ve si los trabajadores encuentran items
        """
        print("\nItems Encontrados:")
        items_encontrados = defaultdict(int)
        for excavador in trabajadores:
            encontro = excavador.encontrar_items(
                *self.arena.probabilidad_encontrar_item())
            if encontro:
                if encontro == parametros.CONSUMIBLE:
                    items_encontrados[parametros.CONSUMIBLE] += 1
                elif encontro == parametros.TESORO:
                    items_encontrados[parametros.TESORO] += 1
                item = random.choice([
                        item for item in self.arena.items
                        if item.tipo == encontro])
                self.mochila.append(item)
                print(f"{excavador.nombre} consiguió {item.nombre}"
                      f" de tipo {item.tipo}.")
            else:
                print(f"{excavador.nombre} no consiguió nada.")
        print(f"Se han encontrado {sum(items_encontrados.values())} ítems:")
        print(f"- {items_encontrados[parametros.CONSUMIBLE]} consumibles")
        print(f"- {items_encontrados[parametros.TESORO]} tesoros")

    def iniciar_evento(self) -> None:
        """
        Ve la ocurrencia de un evento y su efecto
        """
        if random.random() < parametros.PROB_INICIAR_EVENTO:
            pesos = [parametros.PROB_LLUVIA,
                     parametros.PROB_TERREMOTO, parametros.PROB_DERRUMBE]
            evento = random.choices(self.eventos, weights=pesos, k=1)[0]
            nuevo_tipo = self.arena.reaccionar_evento(evento)
            if nuevo_tipo:
                self.arena = seleccionar_arena(nuevo_tipo)
            for excavador in self.equipo:
                excavador.reaccionar_evento()
            print(f"\n¡¡Durante el día da trabajo ocurrió un {evento}!!")
            print(f"La arena final es de tipo {self.arena.tipo}")
            if evento == parametros.DERRUMBE:
                self.metros_cavados -= parametros.METROS_PERDIDOS_DERRUMBE
                print(f"Se han perdido {parametros.METROS_PERDIDOS_DERRUMBE}"
                      " metros de progreso.")
            print(f"Tu equipo ha perdido {parametros.FELICIDAD_PERDIDA}"
                  " de felicidad")
        else:
            print("\nNo ocurrió ningun evento!")

    def editar_energia(self, trabajadores: list, descansando: list):
        """
        Maneja la energia de los excavadores al final del dia
        """
        for excavador in trabajadores:
            excavador.gastar_energia()
            if excavador.energia == 0:
                excavador.descansar()
        for excavador in descansando:
            excavador.descansar()
            print(f"{excavador.nombre} decidió descansar...")

    def mostrar_estado_torneo(self) -> None:
        """
        Imprime el estado del torneo
        """
        separador = "-" * 61
        print(f'\n{"*** Estado Torneo ***":^61}')
        print(separador)
        print(f"Día actual: {self.dias_transcurridos}")
        print(f"Tipo de arena: {self.arena.tipo}")
        print(f"Metros excavados: {self.metros_cavados} / {self.meta}")
        print(separador)
        print(f'{"Excavadores":^61}')
        print(separador)
        f_titulo_excavador = "{:^8} | {:^8} | {:^7} | {:^7} | {:^7} | {:^7}"
        titulo_excavador = ["Nombre", "Tipo", "Energía",
                            "Fuerza", "Suerte", "Felicidad"]
        print(f_titulo_excavador.format(*titulo_excavador))
        print(separador)
        f_excavador = "{:8.8s} | {:<8.8s} | {:^7} | {:^7} | {:^7} | {:^9}"
        for excavador in self.equipo:
            print(f_excavador.format(
                excavador.nombre, excavador.tipo, excavador.energia,
                excavador.fuerza, excavador.suerte, excavador.felicidad))

    def ver_mochila(self) -> None:
        """
        Imprime los items en la mochila
        """
        for i, item in enumerate(self.mochila, 1):
            print(f'{f"[{i}] {item.nombre}":18.18s}|{item.tipo:^12.12s}'
                  f'|{item.descripcion:^49.49s}')

    def usar_consumible(self, posicion: int) -> None:
        """
        Consume un consumible y lo elimina de la mochila
        """
        consumible = self.mochila.pop(posicion)
        for excavador in self.equipo:
            excavador.consumir(consumible)
        print(f"\nSe consumió {consumible.nombre}"
              " entregando los siguientes efectos:")
        print(f"{consumible.descripcion}")

    def abrir_tesoro(self, posicion: int) -> None:
        """
        Abre un tesoro y maneja su efecto
        """
        tesoro = self.mochila.pop(posicion)
        if tesoro.calidad == parametros.CALIDAD_EQUIPO:
            self.equipo.append(agregar_excavador(tesoro.cambio))
            print(f"\nEl tesoro {tesoro.nombre}"
                  f" agrego un excavador de tipo {tesoro.cambio}.")
        else:
            self.arena = seleccionar_arena(tesoro.cambio)
            print(f"\nEl tesoro {tesoro.nombre} cambio el"
                  f" tipo de arena a {tesoro.cambio}.")


def seleccionar_arena(tipo: str):
    """
    Selecciona la arena de juego
    """
    with open(parametros.PATH_ARENAS, 'rt',
              encoding=parametros.ENCODING) as info_arenas:
        arenas = [entidades.crear_arena_juego(
            arena[0], arena[1], int(arena[2]),
            int(arena[3]), int(arena[4]), int(arena[5]))
                  for arena in (
                      linea.strip().split(',')
                      for linea in info_arenas.readlines()[1:])
                  if arena[1] == tipo]
        arena = random.choice(arenas)
        anadir_items(arena)
        return arena


def anadir_items(arena) -> None:
    """
    Añade items a la arena
    """
    with (open(parametros.PATH_CONSUMIBLES,
               'rt', encoding=parametros.ENCODING) as info_consumibles,
          open(parametros.PATH_TESOROS,
               'rt', encoding=parametros.ENCODING) as info_tesoros):
        consumibles = [entidades.Consumible(
            int(consumible[2]), int(consumible[3]), int(consumible[4]),
            int(consumible[5]), consumible[0], parametros.CONSUMIBLE,
            consumible[1])
                       for consumible in
                       (linea.strip().split(',')
                        for linea in info_consumibles.readlines()[1:])]
        tesoros = [entidades.Tesoro(
            int(consumible[2]), consumible[3], consumible[0],
            parametros.TESORO, consumible[1])
                   for consumible in (
                       linea.strip().split(',')
                       for linea in info_tesoros.readlines()[1:])]
        arena.items = consumibles + tesoros


def seleccionar_equipo():
    """
    Selecciona el equipo de excavadores
    """
    with open(parametros.PATH_EXCAVADORES,
              'rt', encoding=parametros.ENCODING) as info_excavadores:
        total_excavadores = [entidades.crear_excavador(
            excavador[0], excavador[1], int(excavador[2]), int(excavador[3]),
            int(excavador[4]), int(excavador[5]), int(excavador[6]))
                             for excavador in (
                                 linea.strip().split(',')
                                 for linea in
                                 info_excavadores.readlines()[1:])]
        return random.sample(
            total_excavadores, k=parametros.CANTIDAD_EXCAVADORES_INICIALES)


def agregar_excavador(tipo: str):
    """
    Selecciona un excavador de un tipo especifico
    """
    with open(parametros.PATH_EXCAVADORES,
              'rt', encoding=parametros.ENCODING) as info_excavadores:
        total_excavadores = [entidades.crear_excavador(
            excavador[0], excavador[1], int(excavador[2]), int(excavador[3]),
            int(excavador[4]), int(excavador[5]), int(excavador[6]))
                             for excavador in (
                                 linea.strip().split(',')
                                 for linea in
                                 info_excavadores.readlines()[1:])
                             if excavador[1] == tipo]
        return random.choice(total_excavadores)


def guardar_partida(torneo, nombre_archivo):
    path = os.path.join(parametros.PATH_PARTIDAS, nombre_archivo +
                        parametros.EXTENSION_PARTIDAS)
    with open(path, "wt",
              encoding=parametros.ENCODING) as f:
        f.write((f"{torneo.metros_cavados},"
                 f"{torneo.dias_transcurridos}\n"))
        arena = (f"{torneo.arena.nombre},{torneo.arena.tipo},"
                 f"{torneo.arena.rareza},{torneo.arena.humedad},"
                 f"{torneo.arena.dureza},{torneo.arena.estatica}\n")
        f.write(arena)
        for item in torneo.mochila:
            if item.tipo == parametros.CONSUMIBLE:
                linea = (f"{item.nombre},{item.tipo},{item.descripcion},"
                         f"{item.energia},{item.fuerza},"
                         f"{item.suerte},{item.felicidad}\n")
            else:
                linea = (f"{item.nombre},{item.tipo},{item.descripcion},"
                         f"{item.calidad},{item.cambio}\n")
            f.write(linea)
        for excavador in torneo.equipo:
            linea = (f"{excavador.nombre},{excavador.tipo},"
                     f"{excavador.edad},{excavador.energia},"
                     f"{excavador.fuerza},{excavador.suerte},"
                     f"{excavador.felicidad},{excavador.descansando}\n")
            f.write(linea)


def cargar_partida(archivo):
    with open(archivo, "rt", encoding=parametros.ENCODING) as partida:
        metros_cavados, dias_transcurridos = (
            partida.readline().strip().split(","))
        metros_cavados, dias_transcurridos = (float(metros_cavados),
                                              int(dias_transcurridos))
        equipo = []
        mochila = []
        for linea in partida.readlines():
            elemento = linea.strip().split(",")
            if elemento[1] in parametros.LISTA_ARENAS:
                arena = entidades.crear_arena_juego(
                    elemento[0], elemento[1], int(elemento[2]),
                    int(elemento[3]), int(elemento[4]), int(elemento[5]))
            elif elemento[1] in parametros.LISTA_ITEMS:
                if elemento[1] == parametros.CONSUMIBLE:
                    item = entidades.Consumible(
                        int(elemento[3]), int(elemento[4]),
                        int(elemento[5]), int(elemento[6]),
                        elemento[0], elemento[1], elemento[2])
                else:
                    item = entidades.Tesoro(int(
                        elemento[3]), elemento[4], elemento[0],
                        elemento[1], elemento[2])
                mochila.append(item)
            else:
                excavador = entidades.crear_excavador(
                    elemento[0], elemento[1], int(elemento[2]),
                    int(elemento[3]), int(elemento[4]), int(elemento[5]),
                    int(elemento[6]))
                excavador.descansando = int(elemento[7])
                equipo.append(excavador)
            anadir_items(arena)
            torneo = Torneo(arena, equipo)
            torneo.metros_cavados = metros_cavados
            torneo.dias_transcurridos = dias_transcurridos
            torneo.equipo = equipo
            torneo.mochila = mochila
        return torneo
