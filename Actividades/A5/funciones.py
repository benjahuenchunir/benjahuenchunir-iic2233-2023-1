from copy import copy
from functools import reduce
from itertools import groupby
from typing import Generator

from utilidades import (
    Categoria, Producto, duplicador_generadores, generador_a_lista
)


# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------

def cargar_productos(ruta: str) -> Generator:
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f.readlines()[1:]:
            id, nombre, precio, pasillo, medida, unidad_medida = linea.strip().split(",")
            yield Producto(int(id), nombre, int(precio), pasillo, int(medida), unidad_medida)


def cargar_categorias(ruta: str) -> Generator:
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f.readlines()[1:]:
            nombre_categoria, id_producto = linea.strip().split(",")
            yield Categoria(nombre_categoria, int(id_producto))


# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------

def obtener_productos(generador_productos: Generator) -> map:
    return map(lambda x: x.nombre, generador_productos)


def obtener_precio_promedio(generador_productos: Generator) -> int:
    copia_generador1, copia_generador2 = duplicador_generadores(generador_productos)
    suma = reduce(lambda x, y: x + y.precio, copia_generador1, 0)
    return int(suma / reduce(lambda x, y: x + 1, copia_generador2, 0))

def filtrar_por_medida(generador_productos: Generator,
                       medida_min: float, medida_max: float, unidad: str
                       ) -> filter:
    return filter(lambda x: x.unidad_medida == unidad and (medida_min < x.medida < medida_max), generador_productos)


def filtrar_por_categoria(generador_productos: Generator,
                          generador_categorias: Generator,
                          nombre_categoria: str) -> filter:
    ids_productos = map(lambda x: x.id_producto, filter(lambda x: x.nombre_categoria == nombre_categoria, generador_categorias))
    lista_ids = generador_a_lista(ids_productos)
    return filter(lambda x: x.id_producto in lista_ids, generador_productos)

def agrupar_por_pasillo(generador_productos: Generator) -> groupby:
    return groupby(generador_productos, key=lambda x: x.pasillo)


# ----------------------------------------------------------------------------
# Parte 3: Iterables
# ----------------------------------------------------------------------------

class Carrito:
    def __init__(self, productos: list) -> None:
        self.productos = productos

    def __iter__(self):
        return IteradorCarrito(self.productos)


class IteradorCarrito:
    def __init__(self, iterable_productos: list) -> None:
        self.productos_iterable = copy(iterable_productos)

    def __iter__(self):
        return self

    def __next__(self):
        print(self.iterable)
        if self.productos_iterable is None:
            raise StopIteration("Llegamos al final")
        else:
            valor = self.productos_iterable
            print(valor)
            self.iterable = valor
            return valor

if __name__ == '__main__':
    def generador_producto():
        yield Producto(1, "Arroz", 200, "Pasillo 1", 1000, "gr")
        yield Producto(5, "Takoyaki", 100, "Pasillo 1", 1000, "ml")
        yield Producto(17, "Mantequilla", 999, "Pasillo 2", 200, "gr")
    
    def test_IteradorCarrito_next():
            productos = list(generador_producto())
            carrito = IteradorCarrito(productos)
            producto_1 = next(carrito)
            producto_2 = next(carrito)
            producto_3 = next(carrito)
            
    test_IteradorCarrito_next()
