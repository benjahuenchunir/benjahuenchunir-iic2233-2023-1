import parametros
import random
from abc import ABC, abstractmethod
from typing import Union


class Item():
    def __init__(self, nombre, tipo, descripcion, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.nombre = nombre
        self.tipo = tipo
        self.descripcion = descripcion


class Consumible(Item):
    def __init__(self, energia, fuerza,
                 suerte, felicidad, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.energia = energia
        self.fuerza = fuerza
        self.suerte = suerte
        self.felicidad = felicidad


class Tesoro(Item):
    def __init__(self, calidad, cambio, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.calidad = calidad
        self.cambio = cambio


class Arena(ABC):
    def __init__(self, nombre, tipo, rareza,
                 humedad, dureza, estatica, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.nombre = nombre
        self.tipo = tipo
        self.rareza = rareza
        self.humedad = humedad
        self.dureza = dureza
        self.estatica = estatica
        self.items = []
        self.dificultad = round(
            (self.rareza + self.humedad + self.dureza + self.estatica) / 40, 2)

    @abstractmethod
    def reaccionar_evento(self, evento: str) -> str:
        pass

    def probabilidad_encontrar_item(self) -> tuple:
        return (parametros.PROB_ENCONTRAR_ITEM, (
            parametros.PROB_ENCONTRAR_TESORO,
            parametros.PROB_ENCONTRAR_CONSUMIBLE))


class ArenaNormal(Arena):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dificultad = round(
            self.dificultad * parametros.POND_ARENA_NORMAL, 2)

    def reaccionar_evento(self, evento: str) -> Union[str, None]:
        if evento == parametros.LLUVIA:
            return parametros.ARENA_MOJADA
        elif evento == parametros.TERREMOTO:
            return parametros.ARENA_ROCOSA
        elif evento == parametros.DERRUMBE:
            return parametros.ARENA_NORMAL


class ArenaMojada(Arena):
    def reaccionar_evento(self, evento: str) -> Union[str, None]:
        if evento == parametros.TERREMOTO:
            return parametros.ARENA_MAGNETICA
        elif evento == parametros.DERRUMBE:
            return parametros.ARENA_NORMAL

    def probabilidad_encontrar_item(self) -> tuple:
        return (parametros.PROB_ENCONTRAR_ITEM_MOJADA, (
            parametros.PROB_CONSUMIBLE_TESORO_MOJADA,
            parametros.PROB_CONSUMIBLE_TESORO_MOJADA))


class ArenaRocosa(Arena):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dificultad = round(
            (self.rareza + self.humedad +
             2 * self.dureza + self.estatica) / 50, 2)

    def reaccionar_evento(self, evento: str) -> Union[str, None]:
        if evento == parametros.LLUVIA:
            return parametros.ARENA_MAGNETICA
        elif evento == parametros.DERRUMBE:
            return parametros.ARENA_NORMAL


class ArenaMagnetica(ArenaRocosa, ArenaMojada):
    def reaccionar_evento(self, evento: str) -> Union[str, None]:
        if evento == parametros.DERRUMBE:
            return parametros.ARENA_NORMAL


class Excavador():
    def __init__(self, nombre: str, tipo: str, edad: int, energia: int,
                 fuerza: int, suerte: int, felicidad: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre = nombre
        self.tipo = tipo
        self.__edad = edad
        self.__energia = energia
        self.__fuerza = fuerza
        self.__suerte = suerte
        self.__felicidad = felicidad
        self.__descansando = 0

    @property
    def edad(self):
        return self.__edad

    @edad.setter
    def edad(self, edad):
        self.__edad = max(18, min(60, edad))

    @property
    def energia(self):
        return self.__energia

    @energia.setter
    def energia(self, energia_restante):
        self.__energia = max(0, min(100, energia_restante))

    @property
    def fuerza(self):
        return self.__fuerza

    @fuerza.setter
    def fuerza(self, nueva_fuerza):
        self.__fuerza = max(1, min(10, nueva_fuerza))

    @property
    def suerte(self):
        return self.__suerte

    @suerte.setter
    def suerte(self, nueva_suerte):
        self.__suerte = max(1, min(10, nueva_suerte))

    @property
    def felicidad(self):
        return self.__felicidad

    @felicidad.setter
    def felicidad(self, nueva_felicidad):
        self.__felicidad = max(1, min(10, nueva_felicidad))

    @property
    def descansando(self):
        return self.__descansando

    @descansando.setter
    def descansando(self, nuevos_dias):
        self.__descansando = max(0, nuevos_dias)

    def cavar(self, dificultad) -> float:
        """
        Calcula los metros cavados y los retorna
        """
        return round(
            (30 / self.edad + (self.felicidad + 2 * self.fuerza)
             / 10) * 1 / (10 * dificultad), 2)

    def descansar(self) -> None:
        """
        Verifica si debe descansar o no
        """
        if self.descansando > 0:
            self.descansando -= 1
            print(f"{self.nombre} esta descansando y le quedan {self.descansando} dias")
            if self.descansando == 0:
                self.energia = 100
                print(f"{self.nombre} termino de descansar ({self.descansando} dias)")
        elif self.energia == 0:
            self.descansando = int(self.edad / 20)
            print(f"{self.nombre} tendra que descansar {self.descansando} dias")

    def encontrar_items(self, probabilidad_encontrar,
                        prob_items) -> Union[str, None]:
        """
        Determina si encuentra un item, retorna None si no lo encuentra
        y el tipo de item en caso contrario
        """
        if random.random() < probabilidad_encontrar:
            tipo_item = random.choices(
                parametros.LISTA_ITEMS, weights=prob_items, k=1)[0]
            return tipo_item

    def gastar_energia(self) -> int:
        """
        Gasta energía al final del día
        """
        gasto = int(10 / self.fuerza + self.edad / 6)
        self.energia -= gasto
        return gasto

    def consumir(self, cosumible: Consumible) -> None:
        """
        Consume un consumible
        """
        self.energia += cosumible.energia
        self.fuerza += cosumible.fuerza
        self.suerte += cosumible.suerte
        self.felicidad += cosumible.felicidad

    def reaccionar_evento(self) -> None:
        """
        Reacciona a un evento
        """
        self.felicidad -= parametros.FELICIDAD_PERDIDA


class ExcavadorDocencio(Excavador):
    def cavar(self, dificultad) -> float:
        metros_cavados = super().cavar(dificultad)
        self.felicidad += parametros.FELICIDAD_ADICIONAL_DOCENCIO
        self.fuerza += parametros.FUERZA_ADICIONAL_DOCENCIO
        return metros_cavados

    def gastar_energia(self) -> int:
        gasto = super().gastar_energia()
        gasto += parametros.ENERGIA_PERDIDA_DOCENCIO
        self.energia -= parametros.ENERGIA_PERDIDA_DOCENCIO
        return gasto


class ExcavadorTareo(Excavador):
    def consumir(self, consumible: Consumible) -> None:
        super().consumir(consumible)
        self.energia += parametros.ENERGIA_ADICIONAL_TAREO
        self.suerte += parametros.SUERTE_ADICIONAL_TAREO
        self.edad += parametros.EDAD_ADICIONAL_TAREO
        self.felicidad -= parametros.FELICIDAD_PERDIDA_TAREO


class ExcavadorHibrido(ExcavadorDocencio, ExcavadorTareo):

    @ExcavadorDocencio.energia.setter
    def energia(self, nueva_energia):
        print(f"{self.nombre} tiene {self.energia} energía")
        self._Excavador__energia = max(20, min(100, nueva_energia))
        print(f"{self.nombre} ahora tiene {self.energia} energía")

    def gastar_energia(self) -> None:
        print(f"{self.nombre} tiene {self.energia} energía")
        energia_inicial = self.energia
        gasto = ExcavadorDocencio.gastar_energia(self)
        print(f"{self.nombre} gasto {int(gasto / 2)} energía")
        self.energia = energia_inicial - int(gasto / 2)
        print(f"{self.nombre} ahora tiene {self.energia} energía")


def crear_arena_juego(nombre: str, tipo: str, rareza: int,
                      humedad: int, dureza: int, estatica: int):
    """
    Decide el tipo de arena que debe crear
    """
    if tipo == parametros.ARENA_NORMAL:
        return ArenaNormal(nombre, tipo, rareza,
                           humedad, dureza, estatica)
    elif tipo == parametros.ARENA_ROCOSA:
        return ArenaRocosa(nombre, tipo, rareza,
                           humedad, dureza, estatica)
    elif tipo == parametros.ARENA_MOJADA:
        return ArenaMojada(nombre, tipo, rareza,
                           humedad, dureza, estatica)
    else:
        return ArenaMagnetica(nombre, tipo, rareza,
                              humedad, dureza, estatica)


def crear_excavador(nombre: str, tipo: str, edad: int,
                    energia: int, fuerza: int, suerte: int, felicidad: int):
    """
    Decide el tipo de excavador que debe crear
    """
    if tipo == parametros.EXCAVADOR_DOCENCIO:
        return ExcavadorDocencio(nombre, tipo, edad, energia,
                                 fuerza, suerte, felicidad)
    elif tipo == parametros.EXCAVADOR_TAREO:
        return ExcavadorTareo(nombre, tipo, edad, energia,
                              fuerza, suerte, felicidad)
    else:
        return ExcavadorHibrido(nombre, tipo, edad, energia,
                                fuerza, suerte, felicidad)
