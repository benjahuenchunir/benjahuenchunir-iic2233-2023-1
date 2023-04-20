from random import random, randint
from threading import Event, Lock, Thread
from time import sleep


class Corredor(Thread):

    TIEMPO_ESPERA = 0.5  # Tiempo entre avances del corredor
    PORCENTAJE_MIN = 70  # Mínimo avance del corredor
    PORCENTAJE_MAX = 100  # Máximo avance del corredor
    PROBABILIDAD_ROBAR = 0.3  # Probabilidad de robar la tortuga

    def __init__(self, nombre: str, tortuga: Lock,
                 senal_inicio: Event, senal_fin: Event,
                 lock_verificar_tortuga: Lock) -> None:
        super().__init__(name=nombre)
        # Referencias al lock de la tortuga y las señales propias de la carrera
        self.name = nombre
        self.lock_tortuga = tortuga
        self.senal_inicio = senal_inicio
        self.senal_fin = senal_fin
        self.lock_verificar_tortuga = lock_verificar_tortuga
        self.tiene_tortuga = False  # Booleano que indica si el corredor lleva la tortuga
        self.__posicion = 0
        self.__velocidad = 10
        self.__correr = True
        self.daemon = True

    @property
    def posicion(self) -> float:
        return self.__posicion

    @posicion.setter
    def posicion(self, nueva_posicion: float) -> None:
        # La posicion no puede aumentar más allá de la meta
        self.__posicion = min(nueva_posicion, 100)

    @property
    def velocidad(self) -> float:
        # El corredor reduce su velocidad si lleva la tortuga
        return self.__velocidad if not self.tiene_tortuga else self.__velocidad * 0.5

    def asignar_rival(self, funcion_notificacion) -> None:
        self.notificar_robo = funcion_notificacion

    def ser_notificado_por_robo(self) -> None:
        self.perder_tortuga()

    def avanzar(self) -> None:
        self.posicion += randint(
            self.PORCENTAJE_MIN * self.velocidad,
            self.PORCENTAJE_MAX * self.velocidad) / 100
        # Luego de avanzar impime su posición y duerme
        print(f'{self.name}: Avancé a {self.posicion:.2f}')
        sleep(self.TIEMPO_ESPERA)

    def intentar_capturar_tortuga(self) -> None:
        # Completar
        if self.lock_tortuga.acquire(blocking=False):
            self.tiene_tortuga = True

        # Si logra la captura, imprime un mensaje
        if self.tiene_tortuga:
            print(f'{self.name}: ¡Capturé la tortuga!')

    def perder_tortuga(self) -> None:
        self.tiene_tortuga = False
        self.lock_tortuga.release()
        print(f'{self.name}: Perdí la tortuga :(')

    def robar_tortuga(self) -> bool:
        # PROBABILIDAD_ROBAR de robar la tortuga
        if random() < self.PROBABILIDAD_ROBAR:
            self.notificar_robo()
            self.lock_tortuga.acquire()
            self.tiene_tortuga = True
            print(f'{self.name}: ¡Robé la tortuga!')
            return True
        else:
            return False

    def correr_primera_mitad(self):
        while self.posicion < 50:
            self.avanzar()

    def correr_segunda_mitad(self) -> bool:
        while self.__correr:
            self.lock_verificar_tortuga.acquire(blocking=True)
            if self.senal_fin.is_set():
                return False
            elif self.posicion >= 100 and self.tiene_tortuga:
                self.senal_fin.set()
                self.lock_tortuga.release()
                return True
            elif not self.tiene_tortuga:
                self.robar_tortuga()
            self.lock_verificar_tortuga.release()
            self.avanzar()

    def run(self) -> None:
        self.senal_inicio.wait()
        self.correr_primera_mitad()
        self.intentar_capturar_tortuga()
        self.correr_segunda_mitad()


class Carrera:
    def __init__(self, corredor_1: Corredor, corredor_2: Corredor, 
                 senal_inicio: Event, senal_fin: Event) -> None:
        super().__init__()
        # Referencias a las señales propias de la carrera
        self.senal_inicio = senal_inicio
        self.senal_fin = senal_fin

        # Guarda los corredores y los asigna como rivales
        self.corredor_1 = corredor_1
        self.corredor_2 = corredor_2
        corredor_1.asignar_rival(corredor_2.ser_notificado_por_robo)
        corredor_2.asignar_rival(corredor_1.ser_notificado_por_robo)
        self.daemon = False

    def empezar(self) -> str:
        self.run()
        if self.corredor_1.tiene_tortuga:
            return self.corredor_1.name
        else:
            return self.corredor_2.name

    def run(self) -> None:
        self.corredor_1.start()
        self.corredor_2.start()
        self.senal_inicio.set()
        self.senal_fin.wait()


if __name__ == '__main__':
    # Instancia una tortuga y las señales
    tortuga = Lock()
    lock_verificar_tortuga = Lock()
    senal_inicio = Event()
    senal_fin = Event()

    # Instancia los corredores y la carrera
    j1 = Corredor('Juan', tortuga, senal_inicio, senal_fin, lock_verificar_tortuga)
    j2 = Corredor('Pepe', tortuga, senal_inicio, senal_fin, lock_verificar_tortuga)
    carrera = Carrera(j1, j2, senal_inicio, senal_fin)

    # Inicia la carrera y pausa el main thread hasta que termine
    ganador = carrera.empezar()

    print(f'{ganador} ha ganado la carrera!!')
