import parametros
import random
from abc import ABC, abstractmethod  # TODO esto esta bien?


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
        pass

    def mostrar_estado_torneo(self):  # TODO hacer bien y bonito
        print("                  *** Estado Torneo ***"
              "-------------------------------------------------------------"
              f"Día actual: {self.dias_transcurridos}"
              "Tipo de arena: Mojada"
              f"Metros excavados: {self.metros_cavados} / {self.dias_totales}"
              "-------------------------------------------------------------"
              "                       Excavadores"
              "-------------------------------------------------------------"
              "    Nombre | Tipo | Energía | Fuerza | Suerte | Felicidad"
              "-------------------------------------------------------------"
              "Lily614 | Docencio | 24 | 20 | 10 | 30"
              "Mpia_vf | Docencio | 55 | 35 | 15 | 25"
              "Beyoncé | Hibrido | 81 | 35 | 20 | 40")
        for excavador in self.equipo:
            print(f"excavador")

    def ver_mochila(self):
        pass

    def usar_consumible(self):
        pass

    def abrir_tesoro(self):
        pass

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
        self.dificultad = 0

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
    def __init__(self, nombre, edad, energia,
                 fuerza, suerte, felicidad, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.nombre = nombre
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
        Calcula los metros cavados
        """
        return round((30 / self.edad + (self.felicidad + 2 * self.fuerza)
                      / 10) * 1 / (10 * dificultad), 2)

    def descanasar(self):
        """
        Calcula los dias que requiere de descanso
        """
        return int(self.edad / 20)

    def encontrar_items(self):
        if random.random() < parametros.PROB_ENCONTRAR_ITEM:
            eventos = ["tesoro", "consumible"]
            pesos = [parametros.PROB_ENCONTRAR_TESORO,
                     parametros.PROB_ENCONTRAR_CONSUMIBLE]
            item_encontrado = random.choices(eventos, weights=pesos, k=1)
            # TODO Encontrar tesoro o consumible
            return item_encontrado

    def gastar_energia(self):
        self.energia -= int(10 / self.fuerza + self.edad / 6)

    def consumir(self, cosumible: Consumible):
        self.energia += cosumible.energia
        self.fuerza += cosumible.fuerza
        self.suerte += cosumible.suerte
        self.felicidad += cosumible.felicidad


class ExcavadorDocencio(Excavador):
    def cavar(self, dificultad):
        metros_cavados = super().cavar(dificultad)
        self.felicidad += parametros.FELICIDAD_ADICIONAL_DOCENCIO
        self.fuerza += parametros.FUERZA_ADICIONAL_DOCENCIO
        self.energia -= parametros.ENERGIA_PERDIDA_DOCENCIO
        return metros_cavados


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
        energia_inicial = self.energia
        ExcavadorDocencio.cavar(self, dificultad)
        self.energia = energia_inicial - parametros.ENERGIA_PERDIDA_DOCENCIO / 2
        # TODO la energia al momento de cavar es solo la de Docencio o la de formula gastar energia?

    def consumir(self, consumible: Consumible):
        ExcavadorTareo.consumir(self, consumible)
