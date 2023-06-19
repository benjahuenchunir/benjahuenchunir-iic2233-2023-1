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
    def __init__(self, socket, id):
        self.socket = socket
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
        self.aceptar_conexiones()
        

        self.turnos = []
        self.turno_actual = 0
        self.valor_anterior = None
        self.valor_actual = None

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
        used_ids = map(lambda x: x.id, self.socket_players.values())
        id = random.choice([nombre for nombre in parametro("ids").values() if nombre not in used_ids])
        self.socket_players[socket_cliente] = Jugador(socket_cliente, id)
        self.mandar_mensaje(Mensaje(parametro("OP_ASIGNAR_NOMBRE"), id), socket_cliente)
        self.mandar_mensaje(Mensaje(parametro("OP_AGREGAR_USUARIOS"), [usuario for usuario in used_ids if usuario != id]), socket_cliente)
        self.mandar_mensaje_a_todos(Mensaje(parametro("OP_AGREGAR_USUARIO"), id))

    def escuchar_cliente(self, socket_cliente: socket.socket) -> None:
        while True:
            try:
                data = socket_cliente.recv(parametro("TAMANO_CHUNKS_BLOQUE"))
                if len(data) > 0:
                    print("Recibiendo mensaje de un cliente")
                    self.manejar_mensaje(self.recibir_mensaje(socket_cliente, data))
                else:
                    print("Usuario desconectado")
                    self.eliminar_cliente(socket_cliente) # TODO esto no se llama sino que si el usuario se va tira exception
                    break
            except Exception:
                print("Hubo algun error")
                self.eliminar_cliente(socket_cliente)
                break

    def eliminar_cliente(self, socket_cliente):
        print("ELiminando cliente")
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
        mensaje_decodificado.extend(mensaje[-parametro("TAMANO_CHUNKS_MENSAJE"):][:largo])
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
        if mensaje == parametro("OP_COMENZAR_PARTIDA"):
            self.comenzar_partida()

    def comenzar_partida(self): # TODO sumar bots
        self.jugando = True
        self.turno_actual = random.randint(0, 1)
        self.turnos = self.sockets.copy()
        data = []
        for socket in self.turnos:
            data.append(self.socket_players[socket].id)
        data.extend(["2", "3", "4"])
        self.mandar_mensaje_a_todos(Mensaje(parametro("OP_AGREGAR_JUGADORES"), data))
        for socket, jugador in self.socket_players.items():
            jugador.lanzar_dados()
            self.mandar_mensaje(Mensaje(parametro("OP_CAMBIAR_DADOS"), (jugador.dado1, jugador.dado2)), socket)

    def jugar_bot(self, bot: Bot):
        if bot.dudar():
            print("Dudando")
        else:
            bot.lanzar_dados()
            if bot.anunciar():
                print("Anunciar")
                

if __name__ == "__main__":
    host = parametro("host")
    port = parametro("port")
    server = Server(host, port)
