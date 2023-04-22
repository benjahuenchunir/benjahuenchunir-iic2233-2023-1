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
    with (open('arenas.csv', 'rt') as info_arenas,
          open('excavadores.csv', 'rt') as info_excavadores):
        arenas = [dccavacava.Arena(
            arena[0], arena[1], arena[2],
            arena[3], arena[4], arena[5])
                  for arena in (
                      linea.strip().split(',')
                      for linea in info_arenas.readlines()[1:])
                  if arena[1] == parametros.ARENA_INICIAL]
        arena_juego = random.choice(arenas)
        total_excavadores = [dccavacava.Excavador(
            excavador[0], excavador[1], excavador[2], excavador[3],
            excavador[4], excavador[5], excavador[6])
                             for excavador in (
                                 linea.strip().split(',')
                                 for linea in
                                 info_excavadores.readlines()[1:])]
        equipo = random.sample(
            total_excavadores, parametros.CANTIDAD_EXCAVADORES_INICIALES)
        torneo = dccavacava.Torneo(arena_juego, equipo)
    return mostrar_menu_principal(torneo)


def cargar_partida():
    return "X" # TODO no implementado
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
            torneo.simular_día()
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
