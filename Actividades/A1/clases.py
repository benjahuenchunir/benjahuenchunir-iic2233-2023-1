from abc import ABC, abstractmethod


class Animal(ABC):
    identificador = 0

    def __init__(self, peso, nombre, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.peso = peso
        self.nombre = nombre
        self.__energia = 100
        self.identificador = Animal.identificador
        Animal.identificador += 1

    @property
    def energia(self) -> int:
        return self.__energia

    @energia.setter
    def energia(self, value):
        self.__energia = max(0, value)

    @abstractmethod
    def desplazarse(self) -> None:
        pass


class Terrestre(Animal):
    def __init__(self, cantidad_patas, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cantidad_patas = cantidad_patas

    def energia_gastada_por_desplazamiento(self) -> int:
        return self.peso * 5

    def desplazarse(self) -> str:
        self.energia -= self.energia_gastada_por_desplazamiento()
        return "caminando..."


class Acuatico(Animal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def energia_gastada_por_desplazamiento(self) -> int:
        return self.peso * 2

    def desplazarse(self) -> str:
        self.energia -= self.energia_gastada_por_desplazamiento()
        return "nadando..."


class Perro(Terrestre):
    def __init__(self, raza, *args, **kwargs) -> None:
        super().__init__(cantidad_patas=4, *args, **kwargs)
        self.raza = raza

    def ladrar(self) -> str:
        return "guau guau"


class Pez(Acuatico):
    def __init__(self, color, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.color = color

    def nadar(self) -> str:
        return "moviendo aleta"


class Ornitorrinco(Acuatico, Terrestre):

    def desplazarse(self) -> str:
        energia = self.energia
        output = Terrestre.desplazarse(self) + Acuatico.desplazarse(self)
        terrestre = Terrestre.energia_gastada_por_desplazamiento(self)
        acuatico = Acuatico.energia_gastada_por_desplazamiento(self)
        self.energia = energia - round((terrestre + acuatico) / 2)
        return output


if __name__ == '__main__':
    perro = Perro(nombre='Pongo', raza='Dalmata', peso=3)
    pez = Pez(nombre='Nemo', color='rojo', peso=1)
    ornitorrinco = Ornitorrinco(nombre='Perry', peso=2, cantidad_patas=6)

    perro.desplazarse()
    pez.desplazarse()
    ornitorrinco.desplazarse()
