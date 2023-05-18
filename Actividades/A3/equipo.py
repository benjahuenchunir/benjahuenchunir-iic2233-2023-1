from collections import defaultdict, deque


class Jugador:
    def __init__(self, nombre: str, velocidad: int) -> None:
        self.nombre = nombre
        self.velocidad = velocidad
    
    def __repr__(self) -> None:
        return f'Jugador: {self.nombre}, Velocidad: {self.velocidad}'


class Equipo:
    def __init__(self) -> None:
        self.jugadores = dict()
        self.dict_adyacencia = defaultdict(set)
    
    def agregar_jugador(self, id_jugador: int, jugador: Jugador) -> bool:
        '''Agrega un nuevo jugador al equipo.'''
        if id_jugador in self.jugadores:
            return False
        else:
            self.jugadores[id_jugador] = jugador
            return True

    def agregar_vecinos(self, id_jugador: int, vecinos: list[int]) -> int:
        '''Agrega una lista de vecinos a un jugador.'''
        if id_jugador not in self.dict_adyacencia:
            return -1

        agregados = 0
        for vecino in vecinos:
            if vecino not in self.dict_adyacencia[id_jugador]:
                self.dict_adyacencia[id_jugador].add(vecino)
                agregados += 1
        return agregados

    def mejor_amigo(self, id_jugador: int) -> Jugador:
        '''Retorna al vecino con la velocidad más similar.'''
        jugador = self.jugadores[id_jugador]
        dif_velocidades = {}
        for id_amigo in self.dict_adyacencia[id_jugador]:
            amigo = self.jugadores[id_amigo]
            dif_velocidades[amigo] = abs(jugador.velocidad - amigo.velocidad)
        return min(dif_velocidades, key=dif_velocidades.get())

    def peor_compañero(self, id_jugador: int) -> Jugador:
        '''Retorna al compañero de equipo con la mayor diferencia de velocidad.'''
        dif_velocidades = {}
        

    def peor_conocido(self, id_jugador: int) -> Jugador:
        '''Retorna al amigo con la mayor diferencia de velocidad.'''
        # Completar
        return "COMPLETAR"
    
    def distancia(self, id_jugador_1: int, id_jugador_2: int) -> int:
        '''Retorna el tamaño del camino más corto entre los jugadores.'''
        # Completar
        return "COMPLETAR"
    

if __name__ == '__main__':
    equipo = Equipo()
    jugadores = {
        0: Jugador('Alonso', 1),
        1: Jugador('Alba', 3),
        2: Jugador('Alicia', 6),
        3: Jugador('Alex', 10)
    }
    adyacencia = {
        0: [1],
        1: [0, 2],
        2: [1],
    }
    for idj, jugador in jugadores.items():
        equipo.agregar_jugador(id_jugador=idj, jugador=jugador)
    for idj, vecinos in adyacencia.items():
        equipo.agregar_vecinos(id_jugador=idj, vecinos=vecinos)
    
    print(f'El mejor amigo de Alba es {equipo.mejor_amigo(1)}') 
    print(f'El peor compañero de Alonso es {equipo.peor_compañero(0)}')
    print(f'El peor amigo de Alicia es {equipo.peor_compañero(2)}')
    print(f'La distancia entre Alicia y Alonso es {equipo.distancia(2, 0)}')
    print(f'La distancia entre Alba y Alex es {equipo.distancia(1, 3)}')
    