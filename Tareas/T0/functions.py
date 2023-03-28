import tablero as funciones_tablero
import os


def cargar_tablero(nombre_archivo: str) -> list:
    path = "Archivos/" + nombre_archivo
    with open(path, "rt") as archivo_tablero:
        tablero_desordenado = archivo_tablero.readline().strip().split(',')
        tablero = []
        fila = []
        for casillero in tablero_desordenado[1:]:
            fila.append(casillero)
            if len(fila) == int(tablero_desordenado[0]):
                tablero.append(fila.copy())
                fila = []
        return tablero


def guardar_tablero(nombre_archivo: str, tablero: list) -> None:
    nombre, extension = os.path.splitext(os.path.basename(nombre_archivo))
    nuevo_nombre = (nombre + "_sol" + extension)
    path = ("Archivos/" + nuevo_nombre)
    with open(path, "wt") as archivo_tablero:
        archivo_tablero.write(
            f"{len(tablero)}," +
            f"{','.join([col for fil in tablero for col in fil])}")


def verificar_valor_bombas(tablero: list) -> int:
    tamaño_maximo = 2 * len(tablero[0]) - 1
    bombas_invalidas = 0
    # [col for fila in tablero for col in fila if col.isdecimal() and (int(col) > tamaño_maximo or int(col) < 2)]
    for fil in tablero:
        for col in fil:
            if col.isdecimal() and (int(col) > tamaño_maximo or int(col) < 2):
                bombas_invalidas += 1
    return bombas_invalidas


def verificar_alcance_bomba(tablero: list, coordenada: tuple) -> int:
    if not tablero[coordenada[0]][coordenada[1]].isdecimal():
        return 0
    rango_explosion = 1
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dx, dy in direcciones:
        y, x = coordenada
        y, x = y + dy, x + dx
        while posicion_valida(tablero, (x, y)):
            rango_explosion += 1
            y, x = y + dy, x + dx
    return rango_explosion


def posicion_valida(tablero, posicion):
    """
    Valida si moverse en cierta direccion es un movimiento valido
    """
    x, y = posicion
    if x < 0 or x >= len(tablero):
        return False
    if y < 0 or y >= len(tablero):
        return False
    if tablero[y][x] == "T":
        return False
    return True


def verificar_tortugas(tablero: list) -> int:
    seguidas = set()
    for y in range(len(tablero)):
        for x in range(len(tablero)):
            if tablero[y][x] != "T":
                continue
            if len(tablero) > (y + 1) and tablero[y + 1][x] == "T":
                seguidas |= {(x, y), (x, y + 1)}
            if len(tablero) > (x + 1) and tablero[y][x + 1] == "T":
                seguidas |= {(x, y), (x + 1, y)}
    return len(seguidas)


def es_valido(tablero: list):
    """
    Verifica que un tablero sea valido (cumpla 2 y 4)
    """
    if verificar_valor_bombas(tablero):
        return False
    if verificar_tortugas(tablero):
        return False
    return True


def es_solucion(tablero: list):
    """
    Verifica que el tablero este solucionado (cumpla 1, 2, 3 y 4)
    """
    if not es_valido(tablero):
        return None
    bombas = ((y, x) for y, fila in enumerate(tablero)
              for x, col in enumerate(fila) if col.isdecimal())
    for y, x in bombas:
        if verificar_alcance_bomba(tablero, (y, x)) != int(tablero[y][x]):
            return False
    else:
        return True


def solucionar_tablero(tablero: list):
    """
    Llama a solucionar el tablero
    (antes se resolvia de forma recursiva aca, pero se demoraba mucho)
    """
    return solucionar_tablero_recursiva(tablero)


def solucionar_tablero_recursiva(tablero: list, pos: tuple = (0, 0)) -> list:
    estado = es_solucion(tablero)
    # Caso base: Es solucion o se invalida
    if estado is True or estado is None:
        return estado
    x0, y0 = pos
    if y0 != len(tablero):  # No ha llegado al final del tablero
        x = (x0 + 1) if x0 < len(tablero) - 1 else 0
        y = y0 + 1 if x == 0 and y0 < len(tablero) else y0
        if tablero[y0][x0] != "-":
            return solucionar_tablero_recursiva(tablero, (x, y))
        for opcion in ["T", "-"]:
            tablero[y0][x0] = opcion
            resultado = solucionar_tablero_recursiva(tablero, (x, y))
            if resultado:
                return tablero


if __name__ == "__main__":
    tablero_2x2 = [
        ['-', 2],
        ['-', '-']
    ]
    resultado = verificar_valor_bombas(tablero_2x2)
    print(resultado)  # Debería ser 0

    resultado = verificar_alcance_bomba(tablero_2x2, (0, 1))
    print(resultado)  # Debería ser 3

    tablero_resuelto = solucionar_tablero(tablero_2x2)
    print(tablero_resuelto)

    tablero_2x2_sol = [
        ['T', 2],
        ['-', '-']
    ]

    resultado = verificar_alcance_bomba(tablero_2x2, (0, 1))
    print(resultado)  # Debería ser 2

    resultado = verificar_tortugas(tablero_2x2_sol)
    print(resultado)  # Debería ser 0
