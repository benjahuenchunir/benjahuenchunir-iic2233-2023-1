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
    def energia(self):
        return self.__energia

    @energia.setter
    def energia(self, value):
        print("Valor", value)
        self.__energia = max(0, value)

    @abstractmethod
    def desplazarse(self) -> None:
        pass


class Terrestre(Animal):
    def __init__(self, cantidad_patas, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cantidad_patas = cantidad_patas

    def energia_gastada_por_desplazamiento(self):
        return self.peso * 5

    def desplazarse(self):
        self.energia -= self.energia_gastada_por_desplazamiento()
        return "caminando..."


class Acuatico(Animal):
    def __init__(self, *args, **kwargs):
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


class Ornitorrinco(Terrestre, Acuatico):

    def desplazarse(self) -> str:
        terrestre = Terrestre.energia_gastada_por_desplazamiento(self)
        acuatico = Acuatico.energia_gastada_por_desplazamiento(self)
        print(f"T: {terrestre} A: {acuatico} Self: {self.energia}")
        self.energia += 2 * terrestre
        self.energia -= int((terrestre + acuatico) / 2)
        print(f"T: {terrestre} A: {acuatico} Self: {self.energia}")
        return Terrestre.desplazarse(self) + Acuatico.desplazarse(self)


if __name__ == '__main__':
    perro = Perro(nombre='Pongo', raza='Dalmata', peso=3)
    pez = Pez(nombre='Nemo', color='rojo', peso=1)
    ornitorrinco = Ornitorrinco(nombre='Perry', peso=2, cantidad_patas=6)

    print("Perro", perro.energia)
    print(perro.desplazarse())
    print(perro.energia)
    print("Pez", pez.energia)
    print(pez.desplazarse())
    print(pez.energia)
    print("Ornitorrinco", ornitorrinco.energia) # T: 2*5, A:2*2 /2
    print(ornitorrinco.desplazarse())
    print(ornitorrinco.energia)
