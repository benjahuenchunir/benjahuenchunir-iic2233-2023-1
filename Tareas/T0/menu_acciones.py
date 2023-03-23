import functions
import tablero as funciones_tablero


def mostrar_menu_acciones(nombre_archivo):  # TODO arreglar el print para que sea bonito
    print("""
    *** Menú de Acciones ***
    [1] Mostrar tablero
    [2] Validar tablero
    [3] Revisar solución
    [4] Solucionar tablero
    [5] Salir del programa\n""")
    opciones = {
        "1":  imprimir_tablero(nombre_archivo),
        "2":  functions.verificar_alcance_bomba()
    }
    seleccion = input("Indique su opción: (1, 2, 3, 4, o 5) ")
    opciones[seleccion]


def imprimir_tablero(nombre_archivo):
    tablero = functions.cargar_tablero(nombre_archivo)
    funciones_tablero.imprimir_tablero(tablero, utf8=True)
