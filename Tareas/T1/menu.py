import parametros
import torneo as f_torneo
import os
import entidades_torneo
from typing import Union


def mostrar_menu_inicio():
    """
    Imprime el menu de inicio
    """
    seleccion = None
    while seleccion != parametros.SALIR:
        print("\n*** Menú de Inicio ***")
        print("-"*22)
        print("[1] Nueva partida\n[2] Cargar Partida\n"
              f"[{parametros.SALIR}] Salir\n")
        seleccion = input("Indique su opción (1, 2, o X):\n")
        if seleccion == "1":
            seleccion = nueva_partida()
        elif seleccion == "2":
            seleccion = mostrar_menu_carga()


def nueva_partida():
    arena = f_torneo.seleccionar_arena(parametros.ARENA_INICIAL)
    equipo = f_torneo.seleccionar_equipo()
    torneo = f_torneo.Torneo(arena, equipo)
    return mostrar_menu_principal(torneo)


def mostrar_menu_principal(torneo):
    """
    Imprime el menu principal
    """
    seleccion = None
    while seleccion != parametros.SALIR:
        print("\n   *** Menú Principal ***\n---------------------------\n")
        print(f"Día torneo DCCavaCava: {torneo.dias_transcurridos}"
              f" / {torneo.dias_totales}")
        print(f"Tipo de arena: {torneo.arena.tipo}")
        print("[1] Simular día torneo\n[2] Ver estado torneo\n[3] Ver ítems\n"
              "[4] Guardar partida\n[5] Volver\n"
              f"[{parametros.SALIR}] Salir del programa")
        seleccion = input("Indique su opción (1, 2, 3, 4 5 o X):\n")
        if seleccion == "1":
            if not torneo.simular_dia():
                return terminar_juego(torneo)
        elif seleccion == "2":
            torneo.mostrar_estado_torneo()
        elif seleccion == "3":
            seleccion = mostrar_menu_items(torneo)
            if seleccion == parametros.SALIR:
                return seleccion
        elif seleccion == "4":
            guardar_partida(torneo)
        elif seleccion == "5":
            return parametros.VOLVER
    return seleccion


def guardar_partida(torneo) -> None:
    nombre_archivo = input("Ingrese el nombre de la partida:\n")
    while not validar_nombre_archivo(nombre_archivo):
        nombre_archivo = input("Ingrese un nombre valido para la partida:\n")
    f_torneo.guardar_partida(torneo, nombre_archivo)
    print("La partida ha sido guardada exitosamente")


def validar_nombre_archivo(nombre_archivo: str) -> Union[bool, None]:
    if nombre_archivo and all(char not in parametros.CARACTERES_INVALIDOS
                              for char in nombre_archivo):
        return True


def terminar_juego(torneo) -> str:
    """
    Imrime el mensaje de fin de juego (victoria o perdida)
    """
    print(f'\n{"El juego ha terminado":^48s}')
    print("-"*48)
    print(f"Metros excavados: {torneo.metros_cavados} / {torneo.meta}")
    if torneo.metros_cavados >= torneo.meta:
        print("Felicidades, ganaste!!!\n")
    else:
        print("Perdiste :(\nVuelve a intentarlo!!\n")
    return parametros.VOLVER


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
        print(f"[{indice_siguiente}] Volver\n"
              f"[{parametros.SALIR}] Salir del programa\n")
        opciones = "Indique su opción ("
        for i in range(indice_siguiente - 1):
            opciones += f"{i}, "
        opciones += f"{indice_siguiente} o X):\n"
        seleccion = input(opciones)
        if seleccion == str(indice_siguiente):
            return parametros.VOLVER
        elif seleccion.isdecimal() and int(seleccion) <= len(torneo.mochila):
            item = torneo.mochila[int(seleccion) - 1]
            if type(item) is entidades_torneo.Consumible:
                torneo.usar_consumible(int(seleccion) - 1)
            else:
                torneo.abrir_tesoro(int(seleccion) - 1)
            return mostrar_menu_items(torneo)
    return seleccion


def mostrar_menu_carga():
    print(f'{"** Menú de carga ***":^22.22s}')
    print("-"*22)
    listado_archivos = os.listdir(parametros.PATH_PARTIDAS)
    for i, archivo in enumerate(listado_archivos, 1):
        print(f'[{i}] {os.path.splitext(archivo)[0]}')
    print(f"[{len(listado_archivos) + 1}] Volver")
    print(f"[{parametros.SALIR}] Salir")
    seleccion = None
    while seleccion != parametros.SALIR:
        seleccion = input("Indique su opción:\n")
        if seleccion == str(len(listado_archivos) + 1):
            return parametros.VOLVER
        if (seleccion.isdecimal() and
                int(seleccion) <= len(listado_archivos)):
            torneo = f_torneo.cargar_partida(
                os.path.join(parametros.PATH_PARTIDAS,
                             listado_archivos[int(seleccion) - 1]))
            return mostrar_menu_principal(torneo)
    return seleccion


if __name__ == "__main__":
    mostrar_menu_inicio()
