import parametros
import random
from abc import ABC, abstractmethod  # TODO esto esta bien?
import menu


class Torneo:
    def __init__(self, arena, equipo, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.arena = arena
        self.equipo = equipo
        self.eventos = ["Terremoto", "Lluvia", "Derrumbe"]
        self.mochila = []
        self.metros_cavados = 0
        self.meta = parametros.METROS_META
        self.dias_transcurridos = 0
        self.dias_totales = parametros.DIAS_TOTALES_TORNEO

    def simular_dia(self):
        for excavador in self.equipo:
            # TODO verificar si tienen energia
            self.metros_cavados += excavador.cavar()
            encontrado = excavador.encontrar_items()
            if encontrado == parametros.TESORO:
                tesoro = random.choice([item for item in self.arena.items
                                        if type(item) is Tesoro])
                self.mochila.append(tesoro)
                # TODO hacer algo con el tesoro
            elif encontrado == parametros.CONSUMIBLE:
                consumible = random.choice([item for item in self.arena.items
                                            if type(item) is Consumible])
                self.mochila.append(consumible)

    def mostrar_estado_torneo(self):  # TODO hacer bien y bonito
        separador = "-" * 61
        print(f'\n{"*** Estado Torneo ***":^61}')
        print(separador)
        print(f"Día actual: {self.dias_transcurridos}")
        print(f"Tipo de arena: {self.arena.tipo}")
        print(f"Metros excavados: {self.metros_cavados} / {self.dias_totales}")
        print(separador)
        print(f'{"Excavadores":^61}')
        print(separador)
        f_titulo_excavador = "{:^8} | {:^8} | {:^7} | {:^7} | {:^7} | {:^7}"
        titulo_excavador = ["Nombre", "Tipo", "Energía",
                            "Fuerza", "Suerte", "Felicidad"]
        print(f_titulo_excavador.format(*titulo_excavador))
        print(separador)
        f_excavador = "{:8.8s} | {:<8.8s} | {:^7} | {:^7} | {:^7} | {:^9}"
        for excavador in self.equipo:
            print(f_excavador.format(
                excavador.nombre, excavador.tipo, excavador.energia,
                excavador.fuerza, excavador.suerte, excavador.felicidad))

    def ver_mochila(self):
        for i, item in enumerate(self.mochila, 1):
            print(f'{f"[{i}] {item.nombre}":^18.18s}|{item.tipo:^12.12s}|{item.descripcion:^49.49s}')

    def usar_consumible(self, posicion: int):
        consumible = self.mochila.pop(posicion)
        for excavador in self.equipo:
            excavador.usar_consumible(consumible)

    def abrir_tesoro(self, posicion: int):
        tesoro = self.mochila.pop(posicion)
        # TODO usar tesoro

    def iniciar_evento(self):
        pass


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


class Arena:
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
        self.dificultad = self.calcular_dificultad()

    def calcular_dificultad(self) -> int:
        pass

    def terremoto(self):
        pass

    def lluvia(self):
        pass


class ArenaNormal(Arena):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dureza = 2*super().dureza


class Excavador():
    def __init__(self, nombre, tipo, edad, energia,
                 fuerza, suerte, felicidad, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.nombre = nombre
        self.tipo = tipo
        self.__edad = edad
        self.__energia = energia
        self.__fuerza = fuerza
        self.__suerte = suerte
        self.__felicidad = felicidad

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

    def cavar(self, dificultad):
        """
        Calcula los metros cavados y los retorna
        """
        metros_cavados = round(
            (30 / self.edad + (self.felicidad + 2 * self.fuerza)
             / 10) * 1 / (10 * dificultad), 2)
        self.gastar_energia()
        return metros_cavados

    def descanasar(self):
        """
        Calcula los dias que requiere de descanso
        """
        return int(self.edad / 20)

    def encontrar_items(self):
        """
        Determina si encuentra un item, retorna None si no lo encuentra
        y el tipo de item en caso contrario
        """
        if random.random() < parametros.PROB_ENCONTRAR_ITEM:
            eventos = [parametros.TESORO, parametros.CONSUMIBLE]
            pesos = [parametros.PROB_ENCONTRAR_TESORO,
                     parametros.PROB_ENCONTRAR_CONSUMIBLE]
            encontrado = random.choices(eventos, weights=pesos, k=1)
            return encontrado

    def gastar_energia(self):
        """
        Gasta energía despues de cavar
        """
        self.energia -= int(10 / self.fuerza + self.edad / 6)

    def consumir(self, cosumible: Consumible):
        """
        Consume un consumible
        """
        self.energia += cosumible.energia
        self.fuerza += cosumible.fuerza
        self.suerte += cosumible.suerte
        self.felicidad += cosumible.felicidad


class ExcavadorDocencio(Excavador):  # TODO revisar implementacion
    def cavar(self, dificultad):
        metros_cavados = super().cavar(dificultad)  # TODO esto toma en cuenta la formula del padre o del hijo
        self.felicidad += parametros.FELICIDAD_ADICIONAL_DOCENCIO
        self.fuerza += parametros.FUERZA_ADICIONAL_DOCENCIO
        self.gastar_energia()
        return metros_cavados

    def gastar_energia(self):
        self.energia -= parametros.ENERGIA_PERDIDA_DOCENCIO


class ExcavadorTareo(Excavador):
    def consumir(self, consumible: Consumible):
        super().consumir(consumible)
        self.energia += parametros.ENERGIA_ADICIONAL_TAREO
        self.suerte += parametros.SUERTE_ADICIONAL_TAREO
        self.edad += parametros.EDAD_ADICIONAL_TAREO
        self.felicidad -= parametros.FELICIDAD_PERDIDA_TAREO


class ExcavadorHibrido(ExcavadorDocencio, ExcavadorTareo):

    @property
    def energia(self):
        return self.__energia

    @energia.setter
    def energia(self, nueva_energia):
        self.__energia = max(20, min(100, nueva_energia))

    def cavar(self, dificultad):
        ExcavadorDocencio.cavar(self, dificultad)

    def consumir(self, consumible: Consumible):
        ExcavadorTareo.consumir(self, consumible)
        
    def gastar_energia(self):
        energia_inicial = self.energia
        gasto = ExcavadorDocencio.gastar_energia(self) + ExcavadorTareo.gastar_energia(self)
        self.energia = energia_inicial - gasto
        # TODO no retorna el gasto energetico

if __name__ == "__main__":
    menu.nueva_partida()