import socket
import random
from threading import Thread
import Scripts.cripto as cr
from utils.utils import parametro, Mensaje
import pickle


class Jugador():
    def __init__(self, socket, id):
        self.socket = socket
        self.id = id
        self.dado1 = None
        self.dado2 = None
        self.vidas = parametro("NUMERO_VIDAS")

    def lanzar_dados(self):
        self.dado1 = random.randint(1, 6)
        self.dado2 = random.randint(1, 6)


class Bot():
    def __init__(self, id):
        self.id = id
        self.dado1 = None
        self.dado2 = None
        self.vidas = parametro("NUMERO_VIDAS")

    def lanzar_dados(self):
        self.dado1 = random.randint(1, 6)
        self.dado2 = random.randint(1, 6)

    def dudar(self):
        return random.random() < parametro("PROB_DUDAR")

    def anunciar(self):
        return random.random() < parametro("PROB_ANUNCIAR")


class Server:
    def __init__(self, host: str, port: int):
        self.sockets = []
        self.socket_players = {}
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.jugando = False
        self.ids = parametro("IDS")
        self.aceptar_conexiones()
        

        self.turnos = []
        self.turno_actual = 0
        self.turnos_totales = 1
        self.valor_anterior = 0
        self.valor_actual = 0

    def aceptar_conexiones(self) -> None:
        thread = Thread(
            target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self) -> None:
        while not self.jugando: # TODO jugador se debe conectar, pero permanecer en ventana inicio
            try:
                print("Esperando que alguien se quiera conectar...")
                socket_cliente, address = self.sock.accept()
                print("Conexión aceptada desde", address)
                self.agregar_cliente(socket_cliente)
                listening_client_thread = Thread(
                    target=self.escuchar_cliente,
                    args=(socket_cliente, ),
                    daemon=True)
                listening_client_thread.start()
            except ConnectionError:
                print("Ocurrió un error.")
            except KeyboardInterrupt:
                print("Interrupcion del usuario")
                self.sock.close()
                break
        print("Cerrando server")
        self.sock.close()

    def agregar_cliente(self, socket_cliente) -> str:
        self.sockets.append(socket_cliente)
        id = self.asignar_id()
        self.mandar_mensaje(Mensaje(parametro("OP_ASIGNAR_NOMBRE"), id), socket_cliente)
        self.mandar_mensaje(Mensaje(parametro("OP_AGREGAR_USUARIOS"), [usuario for usuario in map(lambda x: x.id, self.socket_players.values())]), socket_cliente)
        self.socket_players[socket_cliente] = Jugador(socket_cliente, id)
        self.mandar_mensaje_a_todos(Mensaje(parametro("OP_AGREGAR_USUARIO"), id))

    def escuchar_cliente(self, socket_cliente: socket.socket) -> None:
        while True:
            try:
                data = socket_cliente.recv(parametro("TAMANO_CHUNKS_BLOQUE"))
                if len(data) > 0:
                    print("Recibiendo mensaje de un cliente")
                    if self.jugando:
                        self.manejar_mensaje_juego(self.recibir_mensaje(socket_cliente, data), socket_cliente)
                    else:
                        self.manejar_mensaje(self.recibir_mensaje(socket_cliente, data))
                else:
                    print("Usuario desconectado")
                    self.eliminar_cliente(socket_cliente) # TODO esto no se llama sino que si el usuario se va tira exception
                    break
            except ConnectionError:
                print("Hubo algun error")
                self.eliminar_cliente(socket_cliente)
                break

    def eliminar_cliente(self, socket_cliente):
        print("Eliminando cliente")
        self.ids.append(self.socket_players[socket_cliente].id)
        self.sockets.remove(socket_cliente)
        self.mandar_mensaje_a_todos(Mensaje(parametro("OP_ELIMINAR_USUARIO"), self.socket_players[socket_cliente].id))
        del self.socket_players[socket_cliente]
        print("Cliente eliminado")

    def recibir_mensaje(self, socket_cliente: socket.socket, data: bytes) -> Mensaje:
        largo = int.from_bytes(data, byteorder='little')
        largo_total = (parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")) * (largo // parametro("TAMANO_CHUNKS_MENSAJE") + min(1, largo % parametro("TAMANO_CHUNKS_MENSAJE")))
        bytes_mensaje = socket_cliente.recv(largo_total)
        mensaje_decodificado = self.decodificar_mensaje(bytes_mensaje, largo)
        mensaje_desencriptado = cr.desencriptar(mensaje_decodificado, parametro("N_PONDERADOR"))
        mensaje = pickle.loads(mensaje_desencriptado)
        return mensaje

    def decodificar_mensaje(self, mensaje: bytes, largo: int) -> bytearray:
        mensaje_decodificado = bytearray()
        for i in range(0, len(mensaje) - (parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")), parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")):
            mensaje_decodificado.extend(mensaje[i+parametro("TAMANO_CHUNKS_BLOQUE"):i+parametro("TAMANO_CHUNKS_MENSAJE")+parametro("TAMANO_CHUNKS_BLOQUE")])
        mensaje_decodificado.extend(mensaje[-parametro("TAMANO_CHUNKS_MENSAJE"):][:largo-(parametro("TAMANO_CHUNKS_MENSAJE"))*(largo // parametro("TAMANO_CHUNKS_MENSAJE"))])
        return mensaje_decodificado

    def codificar_mensaje(self, mensaje: bytearray) -> bytearray:
        mensaje_codificado = bytearray(
            len(mensaje).to_bytes(parametro("TAMANO_CHUNKS_BLOQUE"), "little"))
        for i in range(0, len(mensaje), parametro("TAMANO_CHUNKS_MENSAJE")):
            mensaje_codificado.extend(
                i.to_bytes(parametro("TAMANO_CHUNKS_BLOQUE"), "big"))
            chunk = mensaje[i: i + parametro("TAMANO_CHUNKS_MENSAJE")]
            if len(chunk) < parametro("TAMANO_CHUNKS_MENSAJE"):
                chunk.extend(
                    bytearray(parametro("TAMANO_CHUNKS_MENSAJE") - len(chunk)))
            mensaje_codificado.extend(chunk)
        return mensaje_codificado

    def convertir_mensaje(self, mensaje: Mensaje):
        bytes_mensaje = pickle.dumps(mensaje)
        mensaje_encriptado = cr.encriptar(bytes_mensaje, parametro("N_PONDERADOR"))
        return self.codificar_mensaje(mensaje_encriptado)

    def mandar_mensaje_a_todos(self, mensaje: Mensaje,):
        mensaje_codificado = self.convertir_mensaje(mensaje)
        for socket in self.sockets:
            socket.sendall(mensaje_codificado)

    def mandar_mensaje(self, mensaje: Mensaje, socket_cliente: socket.socket):
        mensaje_codificado = self.convertir_mensaje(mensaje)
        socket_cliente.sendall(mensaje_codificado)

    def manejar_mensaje(self, mensaje: Mensaje):
        print(mensaje)
        if mensaje == parametro("OP_COMENZAR_PARTIDA"):
            self.comenzar_partida()
        else:
            print("No existe esa operacion")

    def manejar_mensaje_juego(self, mensaje: Mensaje, socket_cliente):
        print(mensaje)
        if self.socket_players[socket_cliente] != self.turnos[self.turno_actual]:
            return
        if mensaje == parametro("AC_ANUNCIAR_VALOR"):
            self.anunciar_valor(mensaje.data)
        else:
            print("No existe esa operacion")

    def asignar_id(self):
        id = random.choice(self.ids)
        self.ids.remove(id)
        return id

    def comenzar_partida(self): # TODO sumar bots
        self.jugando = True
        self.turnos = list(self.socket_players.values())
        if len(self.turnos) < parametro("NUMERO_JUGADORES"):
            for i in range(parametro("NUMERO_JUGADORES") - len(self.sockets)):
                self.turnos.append(Bot(self.asignar_id()))
        random.shuffle(self.turnos)
        data = []
        for jugador in self.turnos:
            data.append(jugador.id)
        self.mandar_mensaje_a_todos(Mensaje(parametro("OP_AGREGAR_JUGADORES"), data))
        for socket, jugador in self.socket_players.items():
            jugador.lanzar_dados()
            self.mandar_mensaje(Mensaje(parametro("OP_CAMBIAR_DADOS"), (jugador.dado1, jugador.dado2)), socket)
        if isinstance(self.turnos[self.turno_actual], Bot):
            self.jugar_bot(self.turnos[self.turno_actual])

    def jugar_bot(self, bot: Bot):
        if bot.dudar():
            print("Dudando")
        else:
            bot.lanzar_dados()
            if bot.anunciar():
                print("Anunciar")

    def actualizar_turno(self):
        turno_anterior = self.turno_actual
        self.turno_actual = (self.turno_actual + 1) % len(self.turnos)
        self.turnos_totales += 1
        return turno_anterior

    def anunciar_valor(self, valor: str):
        if not valor.isdecimal():
            return
        if int(valor) > self.valor_actual and (1 <= int(valor) <= 12):
            self.valor_anterior = self.valor_actual
            self.valor_actual = int(valor)
            turno_anterior = self.actualizar_turno()
            self.mandar_mensaje_a_todos(
                Mensaje(parametro("OP_CAMBIAR_NUMERO_MAYOR"),
                        str(self.valor_actual)))
            self.mandar_mensaje_a_todos(
                Mensaje(parametro("OP_CAMBIAR_TURNOS"),
                        (self.turnos[self.turno_actual].id,
                         self.turnos[turno_anterior].id,
                         str(self.turnos_totales))))


if __name__ == "__main__":
    host = parametro("host")
    port = parametro("port")
    server = Server(host, port)
