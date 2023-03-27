import os
import functions
import tablero as funciones_tablero


def mostrar_menu_inicio():
    """
    Imprime el menu de inicio y valida el input
    """
    print("*** Menú de Inicio ***\n")
    nombre_archivo = input("Indique el nombre del archivo que desea abrir: ")
    path = "Archivos/" + nombre_archivo  # TODO enter crashea
    if nombre_archivo != "" and os.path.lexists(path):
        mostrar_menu_acciones(nombre_archivo)
    else:
        print("El archivo no existe, cerrando el programa")


def mostrar_menu_acciones(nombre_archivo):
    """
    Imprime el menu de acciones
    """
    seleccion = ""
    while seleccion != "5":
        print("\n*** Menú de Acciones ***\n[1] Mostrar tablero\n"
              "[2] Validar tablero\n[3] Revisar solución\n"
              "[4] Solucionar tablero\n[5] Salir del programa\n")
        seleccion = input("Indique su opción (1, 2, 3, 4, o 5):\n")
        manejar_seleccion(seleccion, nombre_archivo)


def manejar_seleccion(seleccion: str, nombre_archivo):
    """
    Maneja la seleccion del usuario
    """
    tablero = functions.cargar_tablero(nombre_archivo)
    opciones = {"1": imprimir_tablero, "2": validar_tablero,
                "3": revisar_solucion}
    if seleccion == "5":
        print("Cerrando el programa")
    elif seleccion == "4":
        solucionar_tablero(tablero, nombre_archivo)
    elif seleccion in opciones:
        opciones[seleccion](tablero)
    else:
        print("El valor ingresado no corresponde a una de las opciones")


def imprimir_tablero(tablero: list):
    """
    Imprime el tablero
    """
    funciones_tablero.imprimir_tablero(tablero, utf8=True)


def validar_tablero(tablero: list):
    """
    Verifica que un tablero sea valido (cumpla 2 y 4)
    """
    if functions.es_valido(tablero):
        print("El tablero es valido")
    else:
        print("El tablero es invalido")


def revisar_solucion(tablero: list):
    """
    Verifica las reglas 1, 2, 3 y 4
    """
    if functions.es_solucion(tablero):
        print("El tablero esta resuelto")
    else:
        print("El tablero no esta resuelto")


def solucionar_tablero(tablero: list, nombre_archivo: str):
    """
    Intenta solucionar el tablero y lo guarda
    """
    print("Solucionando el tablero...")
    solucion = functions.solucionar_tablero(tablero)
    if solucion is None:
        print("El tablero no se pudo solucionar")
    else:
        funciones_tablero.imprimir_tablero(solucion)
        functions.guardar_tablero(nombre_archivo, tablero)


mostrar_menu_inicio()
