import os
import parametros
import random
import dccavacava


def mostrar_menu_inicio():
    """
    Imprime el menu de inicio
    """
    seleccion = ""
    while seleccion != "X":
        print("*** Menú de Inicio ***\n----------------------\n"
              "[1] Nueva partida\n[2] Cargar Partida\n[X] Salir\n")
        seleccion = input("Indique su opción (1, 2, o X):\n")
        if seleccion == 1:
            nueva_partida()
        elif seleccion == 2:
            cargar_partida()


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
            excavador[0], excavador[2], excavador[3],
            excavador[4], excavador[5], excavador[6])
                             for excavador in (
                                 linea.strip().split(',')
                                 for linea in
                                 info_excavadores.readlines()[1:])]
        equipo = random.sample(
            total_excavadores, parametros.CANTIDAD_EXCAVADORES_INICIALES)


def cargar_partida():
    archivo = "DCCavaCava.txt"
    if os.path.exists(archivo):
        with open(archivo, "rt") as partida:
            # TODO leer archivo
            pass
        mostrar_menu_principal()
    else:
        print("No existe una partida guardada")


def mostrar_menu_principal(arena_juego: dccavacava.Arena, equipo: list):
    """
    Imprime el menu principal
    """
    seleccion = ""
    while seleccion != "X":
        print("   *** Menú Principal ***\n---------------------------\n"
              "[1] Simular día torneo\n[2] Ver estado torneo\n[3] Ver ítems\n"
              "[4] Guardar partida\n[5] Volver\n[X] Salir del programa")
        seleccion = input("Indique su opción (1, 2, 3, 4 5 o X):\n")
        manejar_seleccion_menu_principal(seleccion)


def manejar_seleccion_menu_principal(seleccion: str):
    pass


if __name__ == "__main__":
    mostrar_menu_inicio()
