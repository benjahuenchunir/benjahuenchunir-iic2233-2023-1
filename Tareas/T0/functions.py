# Agregar los imports que estimen necesarios
import tablero as funciones_tablero
import os
import time


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


def verificar_islas(tablero: list) -> bool:
    pass


# Permite validar si moverse en cierta direccion es un movimiento valido
def posicion_valida(tablero, posicion):
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


def solucionar_tablero(tablero: list) -> list:
    estado = es_solucion(tablero)
    # Es invalido o es solucion
    if estado is None or estado is True:
        return estado
    # Probara reemplazar cada guion por una tortuga
    for y in range(len(tablero)):
        for x in range(len(tablero)):
            if tablero[y][x] == "-":
                tablero[y][x] = "T"
                solucion = solucionar_tablero(tablero)
                # Deshacer el cambio porque no es valido
                if solucion is None:
                    tablero[y][x] = "-"
                elif solucion:
                    return tablero  # Los cambios son validos
                
def solucionar_tablero2(tablero: list, pos) -> list:
    estado = es_solucion(tablero)
    funciones_tablero.imprimir_tablero(tablero)
    # Es invalido o es solucion
    if estado is None or estado is True:
        print("Es invalido")
        return estado
    x0, y0 = pos
    # Probara reemplazar cada guion por una tortuga
    for y in range(x0, len(tablero)):
        for x in range(y0, len(tablero)):
            if tablero[y][x] == "-":
                tablero[y][x] = "T"
                print(f"Cambiando {y},{x}")
                solucion = solucionar_tablero2(tablero, (x, y))
                # Deshacer el cambio porque no es valido
                if solucion is None:
                    tablero[y][x] = "-"
                elif solucion:
                    return tablero  # Los cambios son validos

def posicion_validaa(tablero, pos):
    x, y = pos
    if tablero[y][x] != "-":
        return False
    if y >= len(tablero):
        return False
    if x >= len(tablero):
        return (y + 1, 0)

def solucionar_tablero3(tablero: list, pos: tuple = (0, 0)) -> list:
    print(pos)
    funciones_tablero.imprimir_tablero(tablero)
    col0, fil0 = pos
    col = (col0 + 1) if col0 < len(tablero) - 1 else 0
    fil = fil0 + 1 if col == 0 and fil0 < len(tablero) else fil0
    
    print(fil)
    estado = es_solucion(tablero)
    if estado is None or estado is True:
        print("Devolvi 1")
        return estado

    if fil0 == len(tablero):
        print("Devolvi 2")
        return False
    
    if tablero[fil0][col0] != "-":
        print(f"Saltando {tablero[fil0][col0]}")
        return solucionar_tablero3(tablero, (col, fil))
    
    for opcion in ["T", "-"]:
        tablero[fil0][col0] = opcion
        resultado = solucionar_tablero3(tablero, (col, fil))
        if resultado:
            print(f"Solution found:\n{tablero}")
            return tablero
        tablero[fil0][col0] = "-"
    return None


tablero = cargar_tablero("5x5.txt")
funciones_tablero.imprimir_tablero(tablero)
t0 = time.monotonic_ns()
funciones_tablero.imprimir_tablero(solucionar_tablero3(tablero, (0, 0)))
funciones_tablero.imprimir_tablero(cargar_tablero("5x5_sol.txt"))
t1 = time.monotonic_ns()
print(f'{(t1-t0)/1_000_000_000:.10f}')


"""if __name__ == "__main__":
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
    print(resultado)  # Debería ser 0"""
