import random
import dccavacava
import parametros


def seleccionar_arena(tipo: str):
    """
    Selecciona la arena de juego
    """
    with open(parametros.PATH_ARENAS, 'rt', encoding="utf-8") as info_arenas:
        arenas = [crear_arena_juego(
            arena[0], arena[1], int(arena[2]),
            int(arena[3]), int(arena[4]), int(arena[5]))
                  for arena in (
                      linea.strip().split(',')
                      for linea in info_arenas.readlines()[1:])
                  if arena[1] == tipo]
        arena = random.choice(arenas)
        anadir_items(arena)
        return arena


def anadir_items(arena):
    with (open(parametros.PATH_CONSUMIBLES,
               'rt', encoding="utf-8") as info_consumibles,
          open(parametros.PATH_TESOROS,
               'rt', encoding="utf-8") as info_tesoros):
        consumibles = [dccavacava.Consumible(
            int(consumible[2]), int(consumible[3]), int(consumible[4]),
            int(consumible[5]), consumible[0], parametros.CONSUMIBLE,
            consumible[1])
                       for consumible in
                       (linea.strip().split(',')
                        for linea in info_consumibles.readlines()[1:])]
        tesoros = [dccavacava.Tesoro(
            int(consumible[2]), consumible[3],
            consumible[0], parametros.TESORO, consumible[1])
                   for consumible in (
                       linea.strip().split(',')
                       for linea in info_tesoros.readlines()[1:])]
        arena.items.extend(consumibles + tesoros)


def crear_arena_juego(nombre: str, tipo: str, rareza: int,
                      humedad: int, dureza: int, estatica: int):
    """
    Decide el tipo de arena que debe crear
    """
    if tipo == parametros.ARENA_NORMAL:
        return dccavacava.ArenaNormal(nombre, tipo, rareza,
                                      humedad, dureza, estatica)
    elif tipo == parametros.ARENA_ROCOSA:
        return dccavacava.ArenaRocosa(nombre, tipo, rareza,
                                      humedad, dureza, estatica)
    elif tipo == parametros.ARENA_MOJADA:
        return dccavacava.ArenaMojada(nombre, tipo, rareza,
                                      humedad, dureza, estatica)
    else:
        return dccavacava.ArenaMagnetica(nombre, tipo, rareza,
                                         humedad, dureza, estatica)


def seleccionar_equipo():
    """
    Selecciona el equipo de excavadores
    """
    with open(parametros.PATH_EXCAVADORES,
              'rt', encoding="utf-8") as info_excavadores:
        total_excavadores = [crear_excavador(
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
              'rt', encoding="utf-8") as info_excavadores:
        total_excavadores = [crear_excavador(
            excavador[0], excavador[1], int(excavador[2]), int(excavador[3]),
            int(excavador[4]), int(excavador[5]), int(excavador[6]))
                             for excavador in (
                                 linea.strip().split(',')
                                 for linea in
                                 info_excavadores.readlines()[1:])
                             if excavador[1] == tipo]
        return random.choice(total_excavadores)


def crear_excavador(nombre: str, tipo: str, edad: int,
                    energia: int, fuerza: int, suerte: int, felicidad: int):
    """
    Decide el tipo de excavador que debe crear
    """
    if tipo == parametros.EXCAVADOR_DOCENCIO:
        return dccavacava.ExcavadorDocencio(nombre, tipo, edad, energia,
                                            fuerza, suerte, felicidad)
    elif tipo == parametros.EXCAVADDOR_TAREO:
        return dccavacava.ExcavadorTareo(nombre, tipo, edad, energia,
                                         fuerza, suerte, felicidad)
    else:
        return dccavacava.ExcavadorHibrido(nombre, tipo, edad, energia,
                                           fuerza, suerte, felicidad)