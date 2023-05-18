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
        if len(self.dict_adyacencia[id_jugador]) == 0:
            return None
        jugador = self.jugadores[id_jugador]
        dif_velocidades = {}
        for id_amigo in self.dict_adyacencia[id_jugador]:
            amigo = self.jugadores[id_amigo]
            dif_velocidades[amigo] = abs(jugador.velocidad - amigo.velocidad)
        return min(dif_velocidades, key=dif_velocidades.get)

    def peor_compañero(self, id_jugador: int) -> Jugador:
        '''Retorna al compañero de equipo con la mayor diferencia de velocidad.'''
        if len(self.jugadores) == 1:
            return None
        dif_velocidades = {}
        jugador = self.jugadores[id_jugador]
        for conocido in self.jugadores.values():
            if conocido != jugador:
                dif_velocidades[conocido] = abs(jugador.velocidad - conocido.velocidad)
        return max(dif_velocidades, key=dif_velocidades.get)

    def peor_conocido(self, id_jugador: int) -> Jugador:
        visitados = []
        queue = deque([id_jugador])

        while len(queue) > 0:
            id_conocido = queue.popleft()
            jugador = self.jugadores[id_conocido]

            if jugador in visitados:
                continue

            visitados.append(jugador)
            for vecino in self.dict_adyacencia[id_conocido]:
                if vecino not in visitados:
                    queue.append(vecino)

        jugador = self.jugadores[id_jugador]
        dif_velocidades = {}
        for conocido in visitados:
            if conocido != jugador:
                dif_velocidades[conocido] = abs(jugador.velocidad - conocido.velocidad)
        if len(dif_velocidades) == 0:
            return None
        return max(dif_velocidades, key=dif_velocidades.get)

    def distancia(self, id_jugador_1: int, id_jugador_2: int) -> int:
        '''Retorna el tamaño del camino más corto entre los jugadores.'''
        nivel = 0
        distancias = {id_jugador_1: 0}

        visitados = []
        queue = deque([id_jugador_1])

        while len(queue) > 0:
            id_jugador = queue.popleft()

            if id_jugador in visitados:
                continue

            visitados.append(id_jugador)
            nivel = distancias[id_jugador] + 1
            id_vecinos = self.dict_adyacencia[id_jugador]
            for id_vecino in id_vecinos:
                distancias[id_vecino] = nivel
                if id_vecino not in visitados:
                    queue.append(id_vecino)
                
        nivel = 0
        distancias2 = {id_jugador_2: 0}

        visitados = []
        queue = deque([id_jugador_2])

        while len(queue) > 0:
            id_jugador = queue.popleft()

            if id_jugador in visitados:
                continue

            visitados.append(id_jugador)
            nivel = distancias2[id_jugador] + 1
            id_vecinos = self.dict_adyacencia[id_jugador]
            for id_vecino in id_vecinos:
                distancias2[id_vecino] = nivel
                if id_vecino not in visitados:
                    queue.append(id_vecino)

        distancia1 = distancias.get(id_jugador_2, None)
        distancia2 = distancias2.get(id_jugador_1, None)

        if distancia1 is None and distancia2 is None:
            return -1
        elif distancia1 is None:
            return distancia2
        elif distancia2 is None:
            return distancia1
        elif distancia1 < distancia2:
            return distancia1
        else:
            return distancia2

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
    print(f'El peor conocido de Alicia es {equipo.peor_conocido(2)}')
    print(f'La distancia entre Alicia y Alonso es {equipo.distancia(2, 0)}')
    print(f'La distancia entre Alba y Alex es {equipo.distancia(1, 3)}')
