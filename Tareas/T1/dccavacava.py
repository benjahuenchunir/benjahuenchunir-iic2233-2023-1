import parametros
from abc import ABC, abstractmethod  # TODO esto esta bien?


class Torneo:
    def __init__(self, arena, equipo, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.arena = arena
        self.equipo = equipo
        self.eventos = "No se"
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


class Eventos:
    pass


class Excavador:
    def __init__(self, nombre, edad, energia,
                 fuerza, suerte, felicidad, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.nombre = nombre
        self.edad = edad
        self.__energia = energia
        self.fuerza = fuerza
        self.suerte = suerte
        self.__felicidad = felicidad

    @property
    def energia(self):
        return self.__energia
    
    @energia.setter
    def energia(self, energia_restante):
        self.__energia = max(0, energia_restante)

    @property
    def felicidad(self):
        return self.__felicidad

    @felicidad.setter
    def felicidad(self, nueva_felicidad):
        self.__felicidad = max(0, nueva_felicidad)

    def cavar(self):
        pass

    def descanasar(self):
        pass

    def encontrar_items(self):
        pass

    def gastar_energia(self):
        pass

    def consumir(self):
        pass
