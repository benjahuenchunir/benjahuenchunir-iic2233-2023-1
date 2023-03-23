import os
import menu_acciones


def mostrar_menu_inicio():
    print("*** Menú de Inicio ***\n")
    nombre_archivo = input("Indique el nombre del archivo que desea abrir: ")
    while True:
        path = "Archivos/" + nombre_archivo
        if os.path.lexists(path):
            menu_acciones.mostrar_menu_acciones(path)
        else:
            nombre_archivo = input(
                """El nombre ingresado no existe, por favor ingrese otro nombre: """)


mostrar_menu_inicio()
