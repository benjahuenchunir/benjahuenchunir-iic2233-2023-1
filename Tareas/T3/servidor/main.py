import socket
import random
from threading import Thread, Lock
import Scripts.cripto as cr
from utils.utils import (parametro, Mensaje,
                         codificar_mensaje, decodificar_mensaje, log)
import pickle
import time
import sys
from entidades import Bot, Jugador


class Server:
    def __init__(self, host: str, port: int):
        super().__init__()
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
        self.tiempo_restante = parametro("TIEMPO_TURNO")

    def aceptar_conexiones(self) -> None:
        print(f"{'Cliente':^17}|{'Evento':^24}|{'Detalles':^24}")
        print("-" * 17 + "|" + "-" * 24 + "|" + "-" * 24)
        thread = Thread(target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self) -> None:
        while True:
            try:
                socket_cliente, address = self.sock.accept()
                self.manejar_agregar_cliente(socket_cliente)
                listening_client_thread = Thread(
                    target=self.escuchar_cliente, 
                    args=(socket_cliente,), daemon=True)
                listening_client_thread.start()
            except ConnectionError:
                break
        self.sock.close()

    def asignar_id(self):
        id = random.choice(self.ids)
        self.ids.remove(id)
        return id

    def manejar_agregar_cliente(self, socket_cliente):
        self.sockets.append(socket_cliente)
        id = self.asignar_id()
        self.mandar_mensaje(
            Mensaje(parametro("OP_ASIGNAR_NOMBRE"), id), socket_cliente)
        log(id, "Conectarse")
        self.socket_players[socket_cliente] = Jugador(socket_cliente, id)
        if self.jugando:
            self.agregar_cliente_juego(socket_cliente)
        else:
            self.agregar_cliente_inicio(socket_cliente)

    def agregar_cliente_inicio(self, socket_cliente):
        for socket in self.sockets:
            self.actualizar_clientes(socket)
        if len(self.sockets) >= parametro("NUMERO_JUGADORES"):
            self.mandar_mensaje(
                Mensaje(parametro("OP_SALA_LLENA")), socket_cliente)

    def agregar_cliente_juego(self, socket_cliente):
        self.actualizar_clientes(socket_cliente)
        self.mandar_mensaje(
            Mensaje(parametro("OP_PARTIDA_EN_CURSO")), socket_cliente)

    def actualizar_clientes(self, socket_cliente):
        usuarios = [usuario.id
                    for socket, usuario in self.socket_players.items()
                    if socket in self.sockets[:4]]
        self.mandar_mensaje(
            Mensaje(
                parametro("OP_ACTUALIZAR_CLIENTES"), usuarios), socket_cliente)

    def escuchar_cliente(self, socket_cliente: socket.socket) -> None:
        while True:
            try:
                data = socket_cliente.recv(parametro("TAMANO_CHUNKS_BLOQUE"))
                if data:
                    if self.jugando:
                        self.manejar_mensaje_juego(
                            self.recibir_mensaje(
                                socket_cliente, data), socket_cliente)
                    else:
                        self.manejar_mensaje(
                            self.recibir_mensaje(socket_cliente, data))
                else:
                    self.manejar_eliminar_cliente(socket_cliente)
                    break
            except ConnectionError:
                self.manejar_eliminar_cliente(socket_cliente)
                break

    def manejar_eliminar_cliente(self, socket_cliente):
        if self.jugando:
            self.eliminar_cliente_juego(socket_cliente)
        else:
            self.eliminar_cliente(socket_cliente)

    def eliminar_cliente(self, socket_cliente):
        socket_cliente.close()
        jugador = self.socket_players[socket_cliente]
        self.ids.append(jugador.id)
        self.sockets.remove(socket_cliente)
        del self.socket_players[socket_cliente]
        for socket in self.socket_players:
            self.actualizar_clientes(socket)
        log(jugador.id, "Desconexion")

    def eliminar_cliente_juego(self, socket_cliente):
        jugador = self.socket_players[socket_cliente]
        if jugador in self.turnos:
            self.turnos.remove(jugador)
            if self.verificar_ganador():
                self.enviar_ganar()
            elif self.turnos[self.turno_actual] == jugador:
                self.actualizar_turno()
                self.eliminar_cliente(socket_cliente)
        else:
            self.eliminar_cliente(socket_cliente)

    def recibir_mensaje(self, socket_cliente: socket.socket, data: bytes):
        largo = int.from_bytes(data, byteorder="little")
        largo_total = ((
            parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")
        ) * (largo // parametro("TAMANO_CHUNKS_MENSAJE")
             + min(1, largo % parametro("TAMANO_CHUNKS_MENSAJE"))))
        bytes_mensaje = socket_cliente.recv(largo_total)
        mensaje_decodificado = decodificar_mensaje(bytes_mensaje, largo)
        mensaje_desencriptado = cr.desencriptar(
            mensaje_decodificado, parametro("N_PONDERADOR")
        )
        with self.pickle_lock:
            mensaje = pickle.loads(mensaje_desencriptado)
        return mensaje

    def convertir_mensaje(self, mensaje: Mensaje):
        with self.pickle_lock:
            bytes_mensaje = pickle.dumps(mensaje)
        mensaje_encriptado = cr.encriptar(
            bytes_mensaje, parametro("N_PONDERADOR"))
        return codificar_mensaje(mensaje_encriptado)

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

    def manejar_mensaje_juego(self, mensaje: Mensaje, socket_cliente):
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
        elif mensaje == parametro("AC_ENVIAR_SELECCION_USUARIO"):
            self.usar_poder_usuario(socket_cliente, mensaje.data)

    def comenzar_partida(self):
        self.jugando = True
        self.turnos = list(self.socket_players.values())
        if len(self.turnos) < parametro("NUMERO_JUGADORES"):
            for i in range(parametro("NUMERO_JUGADORES") - len(self.sockets)):
                self.turnos.append(Bot(self.asignar_id()))
        random.shuffle(self.turnos)
        data = []
        for jugador in self.turnos:
            data.append(jugador.id)
        log("-", "Inicio partida", ",".join(data))
        self.mandar_mensaje_a_todos(Mensaje(parametro("OP_AGREGAR_JUGADORES"), data))
        self.lanzar_dados_todos()
        self.verificar_turno_bot()

    def jugar_bot(self, bot: Bot):
        jugador_anterior = self.turnos[
            self.obtener_turno_anterior(self.turno_actual)]
        time.sleep(5)
        if jugador_anterior.accion is not None and bot.dudar():
            self.dudar(bot)
        else:
            bot.lanzar_dados()
            valor = random.randint(self.valor_actual + 1, 12)
            if bot.anunciar() and valor < 12:
                self.anunciar_valor(bot, str(valor))
            else:
                self.pasar(bot)

    def verificar_turno_bot(self):
        if isinstance(self.turnos[self.turno_actual], Bot):
            self.jugar_bot(self.turnos[self.turno_actual])

    def actualizar_turno(self, jugador=None):
        self.turno_actual = (self.turno_actual + 1) % len(self.turnos)
        self.turnos_totales += 1
        if jugador is not None:
            self.reiniciar_opciones_jugador(jugador)
        self.mandar_turno(self.turnos[self.turno_actual].id, jugador.id)
        self.verificar_turno_bot()

    def reiniciar_opciones_jugador(self, jugador):
        jugador.puede_cambiar = True
        jugador.puede_dudar = True

    def mandar_turno(self, turno_actual, turno_anterior):
        log(turno_actual, "Comienzo turno")
        self.mandar_mensaje_a_todos(
            Mensaje(parametro("OP_CAMBIAR_TURNOS"),
                    (turno_actual, turno_anterior, str(self.turnos_totales))))

    def lanzar_dados(self, socket, jugador):
        jugador.lanzar_dados()
        self.mandar_mensaje(Mensaje(
            parametro("OP_CAMBIAR_DADOS"), (jugador.dado1, jugador.dado2)),
            socket)

    def lanzar_dados_todos(self):
        for socket, jugador in self.socket_players.items():
            self.lanzar_dados(socket, jugador)
        for bot in self.turnos:
            if isinstance(bot, Bot):
                bot.lanzar_dados()

    def anunciar_valor(self, jugador, valor: str):
        if not valor.isdecimal():
            return
        if int(valor) > self.valor_actual and (1 <= int(valor) <= 12):
            self.valor_anterior = self.valor_actual
            self.valor_actual = int(valor)
            log(jugador.id, "Anunciar valor", f"Valor: {valor}")
            self.mandar_valor()
            self.actualizar_turno(jugador)
            jugador.accion = parametro("AC_ANUNCIAR_VALOR")

    def mostrar_dados(self, socket_cliente):
        dados = [(x.id, (x.dado1, x.dado2)) for x in self.turnos]
        self.mandar_mensaje(
            Mensaje(parametro("OP_MOSTRAR_DADOS"), (dados)), socket_cliente
        )

    def ocultar_dados(self, socket_cliente):
        ids = [x.id for x in self.turnos
               if x != self.socket_players[socket_cliente]]
        self.mandar_mensaje(
            Mensaje(parametro("OP_OCULTAR_DADOS"), ids), socket_cliente)

    def mandar_valor(self):
        self.mandar_mensaje_a_todos(
            Mensaje(parametro("OP_CAMBIAR_NUMERO_MAYOR"), str(self.valor_actual)))

    def pasar(self, jugador):
        jugador.accion = parametro("AC_PASAR_TURNO")
        log(jugador.id, "Pasar")
        self.actualizar_turno(jugador)

    def cambiar_dados(self, socket_cliente: socket.socket):
        jugador = self.socket_players[socket_cliente]
        if jugador.puede_cambiar:
            jugador.puede_dudar = False
            jugador.puede_cambiar = False
            self.lanzar_dados(socket_cliente, jugador)
            log(jugador.id, "Cambiar dados")

    def usar_poder(self, socket_cliente):
        jugador = self.socket_players[socket_cliente]
        if (len(set([jugador.dado1, jugador.dado2, 1, 2])) == 2
                or len(set([jugador.dado1, jugador.dado2, 1, 3])) == 2):
            self.mandar_mensaje(Mensaje(
                    parametro("OP_ELEGIR_USUARIO"),
                    [x.id
                     for x in self.turnos
                     if x != self.socket_players[socket_cliente]],),
                socket_cliente,)

    def usar_poder_usuario(self, socket_cliente, usuario):
        jugador = self.socket_players[socket_cliente]
        objetivo = list(filter(lambda x: x.id == usuario, self.turnos))[0]
        turno = self.turnos.index(objetivo)
        if len(set([jugador.dado1, jugador.dado2, 1, 2])) == 2:
            log(jugador.id, "Usando Ataque", f"Objetivo: {usuario}")
            self.terminar_ronda(objetivo, turno)
        elif len(set([jugador.dado1, jugador.dado2, 1, 3])) == 2:
            log(jugador.id, "Usando Terremoto", f"Objetivo: {usuario}")
            vidas = objetivo.vidas - random.randint(1, parametro("NUMERO_VIDAS"))
            self.terminar_ronda(objetivo, turno, vidas)

    def dudar(self, jugador):
        turno_anterior = self.obtener_turno_anterior(self.turno_actual)
        jugador_anterior = self.turnos[turno_anterior]
        if jugador_anterior.accion is None:
            return
        valor = jugador_anterior.dado1 + jugador_anterior.dado2
        log(jugador.id, "Dudar")
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

    def terminar_ronda(self, perdedor, turno, vidas=1):
        for socket in self.socket_players:
            self.mostrar_dados(socket)
        time.sleep(5)
        for socket in self.socket_players:
            self.ocultar_dados(socket)
        if self.perder_vida(perdedor, vidas):
            if self.verificar_ganador():
                self.enviar_ganar()
            else:
                self.turno_actual = self.obtener_turno_anterior(turno)
                self.reiniciar_ronda()
        else:
            self.turno_actual = turno
            self.reiniciar_ronda()

    def enviar_ganar(self):
        self.mandar_mensaje_a_todos(Mensaje(parametro("OP_GANAR")))
        log("", "Termino partida", f"Ganador: {self.turnos[0].id}")

    def reiniciar_ronda(self):
        self.turnos_totales = 1
        self.mandar_turno(self.turnos[self.turno_actual].id, "-")
        self.valor_actual = 0
        self.mandar_valor()
        for jugador in self.turnos:
            self.reiniciar_jugador(jugador)
        self.lanzar_dados_todos()
        self.verificar_turno_bot()

    def verificar_ganador(self):
        return len(self.turnos) == 1

    def reiniciar_jugador(self, jugador):
        if isinstance(jugador, Jugador):
            self.reiniciar_opciones_jugador(jugador)
        jugador.accion = None

    def obtener_turno_anterior(self, turno):
        return turno - 1 if turno > 0 else len(self.turnos) - 1

    def perder_vida(self, perdedor, vidas):
        perdedor.vidas -= vidas
        log(perdedor.id, "Perdió una vida", f"Quedan: {perdedor.vidas}")
        self.mandar_mensaje_a_todos(
            Mensaje(
                parametro("OP_ACTUALIZAR_VIDA"),
                (perdedor.id, str(perdedor.vidas))))
        if perdedor.vidas == 0:
            if isinstance(perdedor, Jugador):
                socket_cliente = list(
                    filter(lambda x: self.socket_players[x] == perdedor,
                           self.socket_players,))[0]
                self.mandar_mensaje(
                    Mensaje(parametro("OP_PERDER")), socket_cliente)
                self.eliminar_cliente(socket_cliente)
            self.turnos.remove(perdedor)
            return True


if __name__ == "__main__":
    port = int(parametro("PORT")) if len(sys.argv) < 2 else int(sys.argv[1])
    host = parametro("HOST") if len(sys.argv) < 3 else int(sys.argv[2])
    server = Server(host, port)
