import os
import functions
import tablero as funciones_tablero


def mostrar_menu_inicio():
    print("*** Menú de Inicio ***\n")
    nombre_archivo = input("Indique el nombre del archivo que desea abrir: ")
    path = "Archivos/" + nombre_archivo  # TODO enter crashea
    if nombre_archivo != "" and os.path.lexists(path):
        mostrar_menu_acciones(nombre_archivo)
    else:
        print("El archivo no existe, cerrando el programa")


def mostrar_menu_acciones(nombre_archivo):
    tablero = functions.cargar_tablero(nombre_archivo)
    seleccion = ""
    opciones = {"1": imprimir_tablero,
                "2": validar_tablero,
                "3": revisar_solucion,
                "4": solucionar_tablero}
    while seleccion != "5":
        print("\n*** Menú de Acciones ***\n[1] Mostrar tablero\n"
              "[2] Validar tablero\n[3] Revisar solución\n"
              "[4] Solucionar tablero\n[5] Salir del programa\n")
        seleccion = input("Indique su opción: (1, 2, 3, 4, o 5)\n")
        if seleccion in opciones:
            opciones[seleccion](tablero)
        elif seleccion != "5":
            print("El valor ingresado no corresponde a una de las opciones")
    print("Cerrando el programa")


def imprimir_tablero(tablero: list):
    funciones_tablero.imprimir_tablero(tablero, utf8=True)


def validar_tablero(tablero: list):
    if (not functions.verificar_valor_bombas(tablero)
            and not functions.verificar_tortugas(tablero)):
        print("El tablero es valido")
    else:
        print("El tablero es invalido")


def revisar_solucion(tablero: list):
    pass


def solucionar_tablero(tablero: list):
    pass


mostrar_menu_inicio()
