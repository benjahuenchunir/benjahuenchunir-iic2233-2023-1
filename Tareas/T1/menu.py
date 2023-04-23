import os
import parametros
import random
import dccavacava


def mostrar_menu_inicio():
    """
    Imprime el menu de inicio
    """
    seleccion = None
    while seleccion != parametros.SALIR:
        print("\n*** Menú de Inicio ***")
        print("-"*22)
        print("[1] Nueva partida\n[2] Cargar Partida\n[X] Salir\n")
        seleccion = input("Indique su opción (1, 2, o X):\n")
        if seleccion == "1":
            seleccion = nueva_partida()
        elif seleccion == "2":
            seleccion = cargar_partida()


def nueva_partida():
    arena = seleccionar_arena(parametros.ARENA_INICIAL)
    añadir_items(arena)
    equipo = seleccionar_equipo()
    torneo = dccavacava.Torneo(arena, equipo)
    return mostrar_menu_principal(torneo)


def seleccionar_arena(tipo: str):
    """
    Selecciona la arena de juego
    """
    with open(parametros.PATH_ARENAS, 'rt') as info_arenas:
        arenas = [crear_arena_juego(
            arena[0], arena[1], int(arena[2]),
            int(arena[3]), int(arena[4]), int(arena[5]))
                  for arena in (
                      linea.strip().split(',')
                      for linea in info_arenas.readlines()[1:])
                  if arena[1] == tipo]
        return random.choice(arenas)


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


def añadir_items(arena):
    with (open(parametros.PATH_CONSUMIBLES, 'rt') as info_consumibles,
          open(parametros.PATH_TESOROS, 'rt') as info_tesoros):
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


def seleccionar_equipo():
    """
    Selecciona el equipo de excavadores
    """
    with open(parametros.PATH_EXCAVADORES, 'rt') as info_excavadores:
        total_excavadores = [crear_excavador(
            excavador[0], excavador[1], int(excavador[2]), int(excavador[3]),
            int(excavador[4]), int(excavador[5]), int(excavador[6]))
                             for excavador in (
                                 linea.strip().split(',')
                                 for linea in
                                 info_excavadores.readlines()[1:])]
        return random.sample(
            total_excavadores, k=parametros.CANTIDAD_EXCAVADORES_INICIALES)


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


def cargar_partida():
    return "X"  # TODO no implementado
    archivo = "DCCavaCava.txt"
    if os.path.exists(archivo):
        with open(archivo, "rt") as partida:
            # TODO leer archivo
            pass
        mostrar_menu_principal()
    else:
        print("No existe una partida guardada")
    return mostrar_menu_principal(arena_juego, equipo)


def mostrar_menu_principal(torneo):
    """
    Imprime el menu principal
    """
    seleccion = None
    while seleccion != parametros.SALIR:
        print("\n   *** Menú Principal ***\n---------------------------\n"
              "[1] Simular día torneo\n[2] Ver estado torneo\n[3] Ver ítems\n"
              "[4] Guardar partida\n[5] Volver\n[X] Salir del programa")
        seleccion = input("Indique su opción (1, 2, 3, 4 5 o X):\n")
        if seleccion == "1":
            torneo.simular_dia()
        elif seleccion == "2":
            torneo.mostrar_estado_torneo()
        elif seleccion == "3":
            seleccion = mostrar_menu_items(torneo)
            if seleccion == parametros.SALIR:
                return seleccion
        elif seleccion == "4":
            pass  # TODO no implementado
        elif seleccion == "5":
            return parametros.VOLVER
    return seleccion


def mostrar_menu_items(torneo):
    """
    Imprime el menu de items
    """
    seleccion = None
    separador = "-" * 81
    while seleccion != parametros.SALIR:
        print(f'\n{"*** Menú Items ***":^81s}')
        print(separador)
        print(f'{"Nombre":^18s}|{"Tipo":^12s}|{"Descripción":^49s}')
        print(separador)
        torneo.ver_mochila()
        print(separador)
        indice_siguiente = len(torneo.mochila) + 1
        print(f"[{indice_siguiente}] Volver\n[X] Salir del programa\n")
        opciones = "Indique su opción ("
        for i in range(indice_siguiente - 1):
            opciones += f"{i}, "
        opciones += f"{indice_siguiente} o X):\n"
        seleccion = input(opciones)
        if seleccion == str(indice_siguiente):
            return parametros.VOLVER
        elif seleccion.isdecimal() and int(seleccion) <= len(torneo.mochila):
            item = torneo.mochila[int(seleccion) - 1]
            if type(item) is dccavacava.Consumible:
                torneo.usar_consumible(int(seleccion) - 1)
            else:
                torneo.usar_tesoro(int(seleccion) - 1)
        # TODO falta que al usar algo retorne al menu pero actualizado
    return seleccion


if __name__ == "__main__":
    mostrar_menu_inicio()
