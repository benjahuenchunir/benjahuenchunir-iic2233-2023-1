import socket
import random
from threading import Thread, Lock
import Scripts.cripto as cr
from utils.utils import parametro, Mensaje
import pickle
import time


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


class Server:
    def __init__(self, host: str, port: int):
        self.sockets = []
        self.socket_players = {}
        self.host = host
        self.port = port
        self.pickle_lock = Lock()
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
        print(f"{'Cliente':^17}|{'Evento':^24}|{'Detalles':^24}")
        print("-" * 17 + "|" + "-" * 24 + "|" + "-" * 24)
        thread = Thread(
            target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self) -> None:
        while not self.jugando: # TODO jugador se debe conectar, pero permanecer en ventana inicio
            try:
                socket_cliente, address = self.sock.accept()
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
        self.log(id, "Conectarse")

    def escuchar_cliente(self, socket_cliente: socket.socket) -> None:
        while True:
            try:
                data = socket_cliente.recv(parametro("TAMANO_CHUNKS_BLOQUE"))
                if len(data) > 0:
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
        jugador = self.socket_players[socket_cliente]
        self.ids.append(jugador.id)
        self.sockets.remove(socket_cliente)
        self.mandar_mensaje_a_todos(Mensaje(parametro("OP_ELIMINAR_USUARIO"), jugador.id))
        del self.socket_players[socket_cliente]
        self.log(jugador.id, "Desconexion")
    
    def eliminar_cliente_juego(self, socket_cliente): # TODO si se desconecta un cliente que esta jugando, entonces se debe eliminar de turnos y verificar ganador, bots, etc
        jugador = self.socket_players[socket_cliente]
        self.ids.append(jugador.id)
        self.sockets.remove(socket_cliente)
        self.mandar_mensaje_a_todos(Mensaje(parametro("OP_ELIMINAR_USUARIO"), jugador.id))
        del self.socket_players[socket_cliente]
        self.log(jugador.id, "Desconexion")

    def recibir_mensaje(self, socket_cliente: socket.socket, data: bytes) -> Mensaje:
        largo = int.from_bytes(data, byteorder='little')
        largo_total = (parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")) * (largo // parametro("TAMANO_CHUNKS_MENSAJE") + min(1, largo % parametro("TAMANO_CHUNKS_MENSAJE")))
        bytes_mensaje = socket_cliente.recv(largo_total)
        mensaje_decodificado = self.decodificar_mensaje(bytes_mensaje, largo)
        mensaje_desencriptado = cr.desencriptar(mensaje_decodificado, parametro("N_PONDERADOR"))
        with self.pickle_lock:
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
        with self.pickle_lock:
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
        jugador = self.socket_players[socket_cliente]
        if mensaje == parametro("AC_SEE"):
            self.mostrar_dados(socket_cliente)
        elif jugador != self.turnos[self.turno_actual]:
            return
        elif mensaje == parametro("AC_ANUNCIAR_VALOR"):
            self.anunciar_valor(jugador, mensaje.data)
        elif mensaje == parametro("AC_PASAR_TURNO"):
            self.pasar(jugador)
        elif mensaje == parametro("AC_CAMBIAR_DADOS"):
            self.cambiar_dados(socket_cliente)
        elif mensaje == parametro("AC_USAR_PODER"):
            self.usar_poder(socket_cliente)
        elif mensaje == parametro("AC_DUDAR"):
            self.dudar(jugador)
        else:
            print("No existe esa operacion")

    def asignar_id(self):
        id = random.choice(self.ids)
        self.ids.remove(id)
        return id

    def comenzar_partida(self): # TODO recibir conexiones, pero dejarlos en inicio
        self.jugando = True
        self.turnos = list(self.socket_players.values())
        if len(self.turnos) < parametro("NUMERO_JUGADORES"):
            for i in range(parametro("NUMERO_JUGADORES") - len(self.sockets)):
                self.turnos.append(Bot(self.asignar_id()))
        random.shuffle(self.turnos)
        data = []
        for jugador in self.turnos:
            data.append(jugador.id)
        self.log("-", "Inicio partida", ",".join(data))
        self.mandar_mensaje_a_todos(Mensaje(parametro("OP_AGREGAR_JUGADORES"), data))
        for socket, jugador in self.socket_players.items():
            self.lanzar_dados(socket, jugador)
        self.verificar_turno_bot()

    def jugar_bot(self, bot: Bot):
        print("Bot esta jugando")
        jugador_anterior = self.turnos[self.obtener_turno_anterior(self.turno_actual)]
        time.sleep(5)
        if jugador_anterior.accion is not None and bot.dudar():
            self.dudar(bot)
        else:
            bot.lanzar_dados()
            valor = random.randint(self.valor_actual, 12)
            if bot.anunciar() and valor != 12:
                self.anunciar_valor(bot, str(valor))
            else:
                self.pasar(bot)
        print("termino el bot")

    def verificar_turno_bot(self):
        print(type(self.turnos[self.turno_actual]))
        if isinstance(self.turnos[self.turno_actual], Bot):
            self.jugar_bot(self.turnos[self.turno_actual])

    def actualizar_turno(self, jugador):
        self.turno_actual = (self.turno_actual + 1) % len(self.turnos)
        self.turnos_totales += 1
        self.reiniciar_jugador(jugador)
        self.mandar_turno(self.turnos[self.turno_actual].id, jugador.id)
        self.verificar_turno_bot()

    def reiniciar_opciones_jugador(self, jugador):
        jugador.puede_cambiar = True
        jugador.puede_dudar = True

    def mandar_turno(self, turno_actual, turno_anterior):
        self.log(turno_actual, "Comienzo turno")
        self.mandar_mensaje_a_todos(
                Mensaje(parametro("OP_CAMBIAR_TURNOS"),
                        (turno_actual,
                         turno_anterior,
                         str(self.turnos_totales))))

    def lanzar_dados(self, socket, jugador):
        jugador.lanzar_dados()
        self.mandar_mensaje(Mensaje(parametro("OP_CAMBIAR_DADOS"), (jugador.dado1, jugador.dado2)), socket)

    def anunciar_valor(self, jugador, valor: str): # TODO indicar en QLineEdit que el valor es invalido
        if not valor.isdecimal():
            return
        if int(valor) > self.valor_actual and (1 <= int(valor) <= 12):
            self.valor_anterior = self.valor_actual
            self.valor_actual = int(valor)
            self.log(jugador.id, "Anunciar valor", f"Valor: {valor}")
            self.mandar_valor()
            self.actualizar_turno(jugador)
            jugador.accion = parametro("AC_ANUNCIAR_VALOR")

    def mostrar_dados(self, socket_cliente):
        dados = [(x.id, (x.dado1, x.dado2)) for x in self.turnos]
        self.mandar_mensaje(Mensaje(parametro("OP_MOSTRAR_DADOS"), (dados)), socket_cliente)

    def ocultar_dados(self, socket_cliente):
        ids = [x.id for x in self.turnos if x != self.socket_players[socket_cliente]]
        self.mandar_mensaje(Mensaje(parametro("OP_OCULTAR_DADOS"), ids), socket_cliente)

    def mandar_valor(self):
        print("Esperando a mandar valor...")
        self.mandar_mensaje_a_todos(
                Mensaje(parametro("OP_CAMBIAR_NUMERO_MAYOR"),
                        str(self.valor_actual)))
        print("Valor mandado")

    def pasar(self, jugador):
        jugador.accion = parametro("AC_PASAR_TURNO")
        self.log(jugador.id, "Pasar")
        self.actualizar_turno(jugador)

    def cambiar_dados(self, socket_cliente: socket.socket):
        jugador = self.socket_players[socket_cliente]
        if jugador.puede_cambiar:
            jugador.puede_dudar = False
            jugador.puede_cambiar = False
            self.lanzar_dados(socket_cliente, jugador)
            self.log(jugador.id, "Cambiar dados")

    def usar_poder(self, socket_cliente): # TODO preguntar jugador, activar boton solo si tiene los dados
        jugador = self.socket_players[socket_cliente]
        if len(set([jugador.dado1, jugador.dado2, 1, 2])) == 2:
            self.log(jugador.id, "Usando Ataque")
        elif len(set([jugador.dado1, jugador.dado2, 1, 3])) == 2:
            self.log(jugador.id, "Usando Terremoto")

    def dudar(self, jugador):
        turno_anterior = self.obtener_turno_anterior(self.turno_actual)
        jugador_anterior = self.turnos[turno_anterior]
        if jugador_anterior.accion is None:
            return
        valor = jugador_anterior.dado1 + jugador_anterior.dado2
        self.log(jugador.id, "Dudar")
        if jugador_anterior.accion == parametro("AC_ANUNCIAR_VALOR"):
            if valor < self.valor_actual:
                self.terminar_ronda(jugador_anterior, turno_anterior)
            else:
                self.terminar_ronda(jugador, self.turno_actual)
        elif jugador_anterior.accion == parametro("AC_PASAR_TURNO"):
            if valor != parametro("VALOR_PASO"):
                self.terminar_ronda(jugador_anterior, turno_anterior)
            else:
                self.terminar_ronda(jugador, self.turno_actual)

    def terminar_ronda(self, perdedor, turno):
        for socket in self.socket_players: # Mostrar dados por 5 segundos
            self.mostrar_dados(socket)
        time.sleep(5)
        for socket in self.socket_players:
            self.ocultar_dados(socket)
        if self.perder_vida(perdedor):
            if self.verificar_ganador():
                self.mandar_mensaje_a_todos(Mensaje(parametro("OP_GANAR")))
                self.log("", "Termino partida", f"Ganador: {self.turnos[0].id}")
            else:
                self.turno_actual = self.obtener_turno_anterior(turno)
                self.reiniciar_ronda()
        else:
            self.turno_actual = turno
            self.reiniciar_ronda()

    def reiniciar_ronda(self):
        self.turnos_totales = 1
        self.mandar_turno(self.turnos[self.turno_actual].id, "-")
        self.valor_actual = 0
        self.mandar_valor()
        for jugador in self.turnos:
            self.reiniciar_jugador(jugador)
        self.verificar_turno_bot()

    def verificar_ganador(self):
        return len(self.turnos) == 1

    def reiniciar_jugador(self, jugador):
        if isinstance(jugador, Jugador):
            self.reiniciar_opciones_jugador(jugador)
        jugador.accion = None

    def obtener_turno_anterior(self, turno):
        return turno - 1 if turno > 0 else len(self.turnos) - 1

    def perder_vida(self, perdedor):
        perdedor.vidas -= 1
        self.log(perdedor.id, "Perdió una vida", f"Quedan: {perdedor.vidas}")
        self.mandar_mensaje_a_todos(Mensaje(parametro("OP_ACTUALIZAR_VIDA"), (perdedor.id, str(perdedor.vidas))))
        if perdedor.vidas == 0:
            if isinstance(perdedor, Jugador):
                socket_cliente = list(filter(lambda x: self.socket_players[x] == perdedor, self.socket_players))[0]
                self.mandar_mensaje(Mensaje(parametro("OP_PERDER")), socket_cliente)
                self.eliminar_cliente(socket_cliente) # TODO creo que el cliente deberia ser eliminado al cerrar la pestaña, no antes: ojo que entonces es necesario cambiar el mensaje que se envia de a todos a solo los que no han perdido en terminmar partida                
            self.turnos.remove(perdedor) # TODO liberar id?
            return True

    def log(self, usuario, evento, detalles="-"):
        print(f"{usuario:^17.15}|{evento:^24.22}|{detalles:^24}")


if __name__ == "__main__":
    host = parametro("host")
    port = parametro("port")
    server = Server(host, port)
