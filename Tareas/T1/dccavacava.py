import parametros
import random
from abc import ABC, abstractmethod  # TODO esto esta bien?
import menu
from collections import defaultdict


class Torneo:
    def __init__(self, arena, equipo, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.arena = arena
        self.equipo = equipo
        self.eventos = ["Terremoto", "Lluvia", "Derrumbe"]
        self.mochila = []
        self.__metros_cavados = 0
        self.meta = parametros.METROS_META
        self.dias_transcurridos = 0
        self.dias_totales = parametros.DIAS_TOTALES_TORNEO

    @property
    def metros_cavados(self):
        return self.__metros_cavados

    @metros_cavados.setter
    def metros_cavados(self, value):
        self.__metros_cavados = max(0, value)

    def simular_dia(self):
        print(f"\n{f'Día {self.dias_transcurridos}':^53s}")
        print("-"*53)
        trabajadores = [excavador for excavador in self.equipo
                        if not excavador.descansando]
        descansando = [excavador for excavador in self.equipo
                       if excavador.descansando]
        self.cavar(trabajadores)
        self.encontrar_items(trabajadores)
        self.iniciar_evento()
        self.editar_energia(trabajadores, descansando)
        self.dias_transcurridos += 1

    def cavar(self, trabajadores):
        print("Metros Cavados:")
        metros_cavados_dia = 0
        for excavador in trabajadores:
            nuevos_metros_cavados = excavador.cavar(self.arena.dificultad)
            metros_cavados_dia += nuevos_metros_cavados
            self.metros_cavados += nuevos_metros_cavados
            print(f"{excavador.nombre} ha cavado {nuevos_metros_cavados} metros.")
        print(f"El equipo ha cavado {metros_cavados_dia} metros.")

    def encontrar_items(self, trabajadores):
        print("\nItems Encontrados:")
        items_encontrados = defaultdict(int)
        for excavador in trabajadores:
            encontro = excavador.encontrar_items()
            print(encontro)
            if encontro:
                if encontro == parametros.TESORO:
                    items_encontrados[parametros.CONSUMIBLE] += 1
                elif encontro == parametros.TESORO:
                    items_encontrados[parametros.CONSUMIBLE] += 1
                print([
                        item for item in self.arena.items
                        if item.tipo == encontro])
                item = random.choice([
                        item for item in self.arena.items
                        if item.tipo == encontro])
                print(self.arena.items)
                print([item for item in self.arena.items
                      if item.tipo == encontro])
                print(item)
                self.mochila.append(item)
                print(f"{excavador.nombre} consiguió {item.nombre} de tipo {item.tipo}.")
            else:
                print(f"{excavador.nombre} no consiguió nada.")
        print(f"Se han encontrado {sum(items_encontrados.values())} ítems:")
        print(f"- {items_encontrados[parametros.CONSUMIBLE]} consumibles")
        print(f"- {items_encontrados[parametros.TESORO]} tesoros")

    def iniciar_evento(self):
        if random.random() < parametros.PROB_INICIAR_EVENTO:
            eventos = [parametros.LLUVIA, parametros.TERREMOTO, parametros.DERRUMBE]
            pesos = [parametros.PROB_LLUVIA,
                     parametros.PROB_TERREMOTO, parametros.PROB_DERRUMBE]
            evento = random.choices(eventos, weights=pesos, k=1)[0]
            nuevo_tipo = self.arena.reaccionar_evento(evento)
            if nuevo_tipo:
                self.arena = menu.seleccionar_arena(nuevo_tipo)
                menu.añadir_items(self.arena)
            for excavador in self.equipo:
                excavador.reaccionar_evento()
            print(f"\n¡¡Durante el día da trabajo ocurrió un {evento}!")
            print(f"La arena final es de tipo {self.arena.tipo}")
            if evento == parametros.DERRUMBE:
                self.metros_cavados -= parametros.METROS_PERDIDOS_DERRUMBE
                print(f"Se han perdido {parametros.METROS_PERDIDOS_DERRUMBE} metros de progreso.")
            print(f"Tu equipo ha perdido {parametros.FELICIDAD_PERDIDA} de felicidad")
        else:
            print("\nNo ocurrió un evento!")

    def editar_energia(self, trabajadores: list, descansando: list):
        for excavador in trabajadores:
            excavador.descansar()
        for excavador in descansando:
            excavador.descansando -= 1
            print(f"{excavador.nombre} decidió descansar...")

    def mostrar_estado_torneo(self):
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

    def __repr__(self) -> str:
        return f"{self.nombre} de tipo {self.tipo} con energía {self.energia} y fuerza {self.fuerza} y suerte {self.suerte} y felicidad {self.felicidad}"


class Tesoro(Item):
    def __init__(self, calidad, cambio, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.calidad = calidad
        self.cambio = cambio

    def __repr__(self) -> str:
        return f"{self.nombre} de tipo {self.tipo} con calidad {self.calidad} y cambio {self.cambio}"


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
    def reaccionar_evento(self, evento: str):
        pass


class ArenaNormal(Arena):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dificultad = round(
            self.dificultad * parametros.POND_ARENA_NORMAL, 2)

    def reaccionar_evento(self, evento: str):
        if evento == parametros.LLUVIA:
            return parametros.ARENA_MOJADA
        elif evento == parametros.TERREMOTO:
            return parametros.ARENA_ROCOSA
        elif evento == parametros.DERRUMBE:
            return parametros.ARENA_NORMAL


class ArenaMojada(Arena):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # TODO implementar propio de mojada

    def reaccionar_evento(self, evento: str):
        if evento == parametros.TERREMOTO:
            return parametros.ARENA_MAGNETICA
        elif evento == parametros.DERRUMBE:
            return parametros.ARENA_NORMAL


class ArenaRocosa(Arena):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dificultad = round(
            (self.rareza + self.humedad +
             2 * self.dureza + self.estatica) / 50, 2)

    def reaccionar_evento(self, evento: str):
        if evento == parametros.LLUVIA:
            return parametros.ARENA_MAGNETICA
        elif evento == parametros.DERRUMBE:
            return parametros.ARENA_NORMAL


class ArenaMagnetica(ArenaRocosa, ArenaMojada):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def reaccionar_evento(self, evento: str):
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

    def cavar(self, dificultad):
        """
        Calcula los metros cavados y los retorna
        """
        return round(
            (30 / self.edad + (self.felicidad + 2 * self.fuerza)
             / 10) * 1 / (10 * dificultad), 2)

    def descansar(self):
        """
        Verifica si debe descansar o no
        """
        if self.energia == 0:
            self.descansando = int(self.edad / 20)
            # TODO por ahora un excavador descansa indefinidamente porque resetea siempre los dias de descanso

    def encontrar_items(self):
        """
        Determina si encuentra un item, retorna None si no lo encuentra
        y el tipo de item en caso contrario
        """
        if random.random() < parametros.PROB_ENCONTRAR_ITEM:
            eventos = [parametros.TESORO, parametros.CONSUMIBLE]
            pesos = [parametros.PROB_ENCONTRAR_TESORO,
                     parametros.PROB_ENCONTRAR_CONSUMIBLE]
            encontrado = random.choices(eventos, weights=pesos, k=1)[0]
            return encontrado

    def gastar_energia(self) -> int:
        """
        Gasta energía al final del día
        """
        gasto = int(10 / self.fuerza + self.edad / 6)
        self.energia -= gasto
        return gasto

    def consumir(self, cosumible: Consumible):
        """
        Consume un consumible
        """
        self.energia += cosumible.energia
        self.fuerza += cosumible.fuerza
        self.suerte += cosumible.suerte
        self.felicidad += cosumible.felicidad

    def reaccionar_evento(self):
        """
        Reacciona a un evento
        """
        self.felicidad -= parametros.FELICIDAD_PERDIDA


class ExcavadorDocencio(Excavador):
    def cavar(self, dificultad):
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
    def consumir(self, consumible: Consumible):
        super().consumir(consumible)
        self.energia += parametros.ENERGIA_ADICIONAL_TAREO
        self.suerte += parametros.SUERTE_ADICIONAL_TAREO
        self.edad += parametros.EDAD_ADICIONAL_TAREO
        self.felicidad -= parametros.FELICIDAD_PERDIDA_TAREO


class ExcavadorHibrido(ExcavadorDocencio, ExcavadorTareo):

    @property
    def energia(self):
        return self._Excavador__energia

    @energia.setter
    def energia(self, nueva_energia):
        self.__energia = max(20, min(100, nueva_energia))

    def cavar(self, dificultad):
        return ExcavadorDocencio.cavar(self, dificultad)

    def consumir(self, consumible: Consumible):
        ExcavadorTareo.consumir(self, consumible)

    def gastar_energia(self):
        energia_inicial = self.energia
        gasto = ExcavadorDocencio.gastar_energia(self)
        self.energia = energia_inicial - int(gasto / 2)


if __name__ == "__main__":
    menu.nueva_partida()
