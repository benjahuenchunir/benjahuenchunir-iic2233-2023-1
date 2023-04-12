import os


def mostrar_menu_inicio():
    """
    Imprime el menu de inicio
    """
    seleccion = ""
    while seleccion != "X":
        print("*** Menú de Inicio ***\n----------------------\n"
              "[1] Nueva partida\n[2] Cargar Partida\n[X] Salir\n")
        seleccion = input("Indique su opción (1, 2, o X):\n")


def mostrar_menu_inicio():
    """
    Imprime el menu principal
    """
    print("   *** Menú Principal ***\n--------------------------\n"
          "[1] Simular día torneo\n[2] Ver estado torneo\n[3] Ver ítems\n"
          "[4] Guardar partida\n [5] Volver\n [X] Salir del programa")
    seleccion = input("Indique su opción (1, 2, 3, 4 5 o X):\n")
