import os
import parametros
import random


def mostrar_menu_inicio():
    """
    Imprime el menu de inicio
    """
    seleccion = ""
    while seleccion != "X":
        print("*** Menú de Inicio ***\n----------------------\n"
              "[1] Nueva partida\n[2] Cargar Partida\n[X] Salir\n")
        seleccion = input("Indique su opción (1, 2, o X):\n")
        manejar_seleccion_menu_inicio(seleccion)


def manejar_seleccion_menu_inicio(seleccion: str):
    if seleccion == "1":
        with (open('arenas.csv', 'rt') as info_arenas,
              open('excavadores.csv', 'rt') as info_excavadores):
            arenas = ((arena.strip().split(',')
                       for arena in info_arenas.readlines()[1:]))
            arena_juego = random.choice(([arena for arena in arenas if arena[1]
                                          == parametros.ARENA_INICIAL]))
            total_excavadores = [(excavador.strip().split(',')
                                  for excavador in info_excavadores.readlines()
                                  )]
            excavadores_juego = random.choices(
                total_excavadores, k=parametros.CANTIDAD_EXCAVADORES_INICIALES)
        mostrar_menu_principal(arena_juego, excavadores_juego)
    elif seleccion == "2":
        pass


def mostrar_menu_principal(arena_juego: list, excavadores_juego: list):
    """
    Imprime el menu principal
    """
    seleccion = ""
    while seleccion != "X":
        print("   *** Menú Principal ***\n--------------------------\n"
              "[1] Simular día torneo\n[2] Ver estado torneo\n[3] Ver ítems\n"
              "[4] Guardar partida\n [5] Volver\n [X] Salir del programa")
        seleccion = input("Indique su opción (1, 2, 3, 4 5 o X):\n")


def manejar_seleccion_menu_principal(seleccion: str):
    pass


mostrar_menu_inicio()