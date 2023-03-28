import os


def cargar_tablero(nombre_archivo: str) -> list:
    """
    Convierte un archivo a un tablero
    """
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
    """
    Guarda el tablero a un archivo
    """
    nombre, extension = os.path.splitext(os.path.basename(nombre_archivo))
    nuevo_nombre = (nombre + "_sol" + extension)
    path = ("Archivos/" + nuevo_nombre)
    with open(path, "wt") as archivo_tablero:
        archivo_tablero.write(
            f"{len(tablero)}," +
            f"{','.join([col for fil in tablero for col in fil])}")


def verificar_valor_bombas(tablero: list) -> int:
    """
    Verifica regla 2
    """
    tamaño_maximo = 2 * len(tablero[0]) - 1
    bombas_invalidas = 0
    for fil in tablero:
        for col in fil:
            if col.isdecimal() and (int(col) > tamaño_maximo or int(col) < 2):
                bombas_invalidas += 1
    return bombas_invalidas


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


def verificar_alcance_bomba(tablero: list, coordenada: tuple) -> int:
    """
    Verifica que la bomba tenga el alcance correcto
    """
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


def verificar_tortugas(tablero: list) -> int:
    """
    Verifica regla 4
    """
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
    if es_solucion(tablero):
        return tablero
    else:
        return solucionar_tablero_recursiva(tablero)


def solucionar_tablero_recursiva(tablero: list, pos: tuple = (0, 0)) -> list:
    estado = es_solucion(tablero)
    # Caso base: Es solución o se invalida
    if estado is True or estado is None:
        return estado
    x_0, y_0 = pos
    # Verificar si llegó al final del tablero
    if y_0 != len(tablero):
        x = (x_0 + 1) if x_0 < len(tablero) - 1 else 0
        y = y_0 + 1 if x == 0 and y_0 < len(tablero) else y_0
        # Saltarse las posiciones que no sean "-"
        if tablero[y_0][x_0] != "-":
            return solucionar_tablero_recursiva(tablero, (x, y))
        # Prueba la posición con y sin tortuga
        for opcion in ["T", "-"]:
            tablero[y_0][x_0] = opcion
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
