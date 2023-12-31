import parametros
import random
from abc import ABC, abstractmethod  # TODO esto esta bien?
from collections import defaultdict
import torneo


class Torneo:
    def __init__(self, arena, equipo, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.arena = arena
        self.equipo = equipo
        self.eventos = [parametros.LLUVIA, parametros.TERREMOTO,
                        parametros.DERRUMBE]
        self.mochila = []
        self.__metros_cavados = 0
        self.meta = parametros.METROS_META
        self.dias_transcurridos = 1
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
        if self.dias_transcurridos <= self.dias_totales:
            return True

    def cavar(self, trabajadores) -> None:
        print(f"Metros Cavados: {self.metros_cavados}")
        metros_cavados_dia = 0
        for excavador in trabajadores:
            nuevos_metros_cavados = excavador.cavar(self.arena.dificultad)
            metros_cavados_dia += nuevos_metros_cavados
            self.metros_cavados += nuevos_metros_cavados
            print(f"{excavador.nombre} ha cavado"
                  f" {nuevos_metros_cavados} metros.")
        print(f"El equipo ha cavado {metros_cavados_dia} metros.")

    def encontrar_items(self, trabajadores) -> None:
        print("\nItems Encontrados:")
        items_encontrados = defaultdict(int)
        for excavador in trabajadores:
            encontro = excavador.encontrar_items(
                *self.arena.probabilidad_encontrar_item())
            if encontro:
                if encontro == parametros.CONSUMIBLE:
                    items_encontrados[parametros.CONSUMIBLE] += 1
                elif encontro == parametros.TESORO:
                    items_encontrados[parametros.TESORO] += 1
                item = random.choice([
                        item for item in self.arena.items
                        if item.tipo == encontro])
                self.mochila.append(item)
                print(f"{excavador.nombre} consiguió {item.nombre}"
                      f" de tipo {item.tipo}.")
            else:
                print(f"{excavador.nombre} no consiguió nada.")
        print(f"Se han encontrado {sum(items_encontrados.values())} ítems:")
        print(f"- {items_encontrados[parametros.CONSUMIBLE]} consumibles")
        print(f"- {items_encontrados[parametros.TESORO]} tesoros")

    def iniciar_evento(self) -> None:
        if random.random() < parametros.PROB_INICIAR_EVENTO:
            pesos = [parametros.PROB_LLUVIA,
                     parametros.PROB_TERREMOTO, parametros.PROB_DERRUMBE]
            evento = random.choices(self.eventos, weights=pesos, k=1)[0]
            nuevo_tipo = self.arena.reaccionar_evento(evento)
            if nuevo_tipo:
                self.arena = torneo.seleccionar_arena(nuevo_tipo)
            for excavador in self.equipo:
                excavador.reaccionar_evento()
            print(f"\n¡¡Durante el día da trabajo ocurrió un {evento}!!")
            print(f"La arena final es de tipo {self.arena.tipo}")
            if evento == parametros.DERRUMBE:
                self.metros_cavados -= parametros.METROS_PERDIDOS_DERRUMBE
                print(f"Se han perdido {parametros.METROS_PERDIDOS_DERRUMBE}"
                      " metros de progreso.")
            print(f"Tu equipo ha perdido {parametros.FELICIDAD_PERDIDA}"
                  " de felicidad")
        else:
            print("\nNo ocurrió ningun evento!")

    def editar_energia(self, trabajadores: list, descansando: list):
        for excavador in trabajadores:
            excavador.gastar_energia()
            if excavador.energia == 0:
                excavador.descansar()
        for excavador in descansando:
            excavador.descansar()
            print(f"{excavador.nombre} decidió descansar...")

    def mostrar_estado_torneo(self) -> None:
        separador = "-" * 61
        print(f'\n{"*** Estado Torneo ***":^61}')
        print(separador)
        print(f"Día actual: {self.dias_transcurridos}")
        print(f"Tipo de arena: {self.arena.tipo}")
        print(f"Metros excavados: {self.metros_cavados} / {self.meta}")
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

    def ver_mochila(self) -> None:
        for i, item in enumerate(self.mochila, 1):
            print(f'{f"[{i}] {item.nombre}":18.18s}|{item.tipo:^12.12s}'
                  f'|{item.descripcion:^49.49s}')

    def usar_consumible(self, posicion: int) -> None:
        consumible = self.mochila.pop(posicion)
        for excavador in self.equipo:
            excavador.consumir(consumible)
        print(f"\nSe consumió {consumible.nombre}"
              " entregando los siguientes efectos:")
        print(f"{consumible.descripcion}")

    def abrir_tesoro(self, posicion: int) -> None:
        tesoro = self.mochila.pop(posicion)
        if tesoro.calidad == parametros.CALIDAD_EQUIPO:
            self.equipo.append(torneo.agregar_excavador(tesoro.cambio))
            print(f"\nEl tesoro {tesoro.nombre}"
                  f" agrego un excavador de tipo {tesoro.cambio}.")
        else:
            self.arena = torneo.seleccionar_arena(tesoro.cambio)
            print(f"\nEl tesoro {tesoro.nombre} cambio el"
                  f" tipo de arena a {tesoro.cambio}.")


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

    def probabilidad_encontrar_item(self) -> float:
        return (parametros.PROB_ENCONTRAR_ITEM, (
            parametros.PROB_ENCONTRAR_TESORO,
            parametros.PROB_ENCONTRAR_CONSUMIBLE))


class ArenaNormal(Arena):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dificultad = round(
            self.dificultad * parametros.POND_ARENA_NORMAL, 2)

    def reaccionar_evento(self, evento: str) -> str:
        if evento == parametros.LLUVIA:
            return parametros.ARENA_MOJADA
        elif evento == parametros.TERREMOTO:
            return parametros.ARENA_ROCOSA
        elif evento == parametros.DERRUMBE:
            return parametros.ARENA_NORMAL


class ArenaMojada(Arena):
    def reaccionar_evento(self, evento: str) -> str:
        if evento == parametros.TERREMOTO:
            return parametros.ARENA_MAGNETICA
        elif evento == parametros.DERRUMBE:
            return parametros.ARENA_NORMAL

    def probabilidad_encontrar_item(self) -> float:
        return (parametros.PROB_ENCONTRAR_ITEM_MOJADA, (
            parametros.PROB_CONSUMIBLE_TESORO_MOJADA,
            parametros.PROB_CONSUMIBLE_TESORO_MOJADA))


class ArenaRocosa(Arena):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dificultad = round(
            (self.rareza + self.humedad +
             2 * self.dureza + self.estatica) / 50, 2)

    def reaccionar_evento(self, evento: str) -> str:
        if evento == parametros.LLUVIA:
            return parametros.ARENA_MAGNETICA
        elif evento == parametros.DERRUMBE:
            return parametros.ARENA_NORMAL


class ArenaMagnetica(ArenaRocosa, ArenaMojada):
    def reaccionar_evento(self, evento: str) -> str:
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

    def encontrar_items(self, probabilidad_encontrar, prob_items) -> str:
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

    def gastar_energia(self) -> int:
        print(f"{self.nombre} tiene {self.energia} energía")
        energia_inicial = self.energia
        gasto = ExcavadorDocencio.gastar_energia(self)
        print(f"{self.nombre} gasto {int(gasto / 2)} energía")
        self.energia = energia_inicial - int(gasto / 2)
        print(f"{self.nombre} ahora tiene {self.energia} energía")
