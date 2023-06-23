import random
from utils.utils import parametro


class Jugador():
    def __init__(self, socket, id):
        self.socket = socket
        self.id = id
        self.dado1 = None
        self.dado2 = None
        self.vidas = parametro("NUMERO_VIDAS")
        self.puede_cambiar = True
        self.puede_dudar = True
        self.accion = None

    def lanzar_dados(self):
        self.dado1 = random.randint(1, 6)
        self.dado2 = random.randint(1, 6)


class Bot():
    def __init__(self, id):
        self.id = id
        self.dado1 = None
        self.dado2 = None
        self.vidas = parametro("NUMERO_VIDAS")
        self.accion = None

    def lanzar_dados(self):
        self.dado1 = random.randint(1, 6)
        self.dado2 = random.randint(1, 6)

    def dudar(self):
        return random.random() < parametro("PROB_DUDAR")

    def anunciar(self):
        return random.random() < parametro("PROB_ANUNCIAR")