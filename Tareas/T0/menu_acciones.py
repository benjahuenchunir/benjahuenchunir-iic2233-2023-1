import functions
import tablero as funciones_tablero


def mostrar_menu_acciones(nombre_archivo):  # TODO arreglar el print para que sea bonito
    tablero = functions.cargar_tablero(nombre_archivo)
    seleccion = ""
    opciones = {
            "1": imprimir_tablero(tablero),
            "2": validar_tablero(tablero),
            "3": revisar_solucion(),
            "4": solucionar_tablero()
        }
    while seleccion != "5":
        print("""
        *** Menú de Acciones ***
        [1] Mostrar tablero
        [2] Validar tablero
        [3] Revisar solución
        [4] Solucionar tablero
        [5] Salir del programa\n""")
        seleccion = input("Indique su opción: (1, 2, 3, 4, o 5)\n")
        if seleccion in opciones.keys():
            print("Entre")
            opciones[seleccion]
        else:
            print("El valor ingresado no corresponde a una de las opciones")


def imprimir_tablero(tablero: list):
    funciones_tablero.imprimir_tablero(tablero, utf8=True)


def validar_tablero(tablero: list):
    print(functions.verificar_valor_bombas(tablero))


def revisar_solucion(tablero: list):
    pass


def solucionar_tablero(tablero: list):
    pass
