from PyQt5.QtGui import QPixmap, QMouseEvent, QFont, QKeyEvent, QKeySequence
from PyQt5.QtWidgets import (
    QListWidgetItem,
    QMessageBox,
    QAbstractItemView,
    QStackedWidget,
    QWidget,
    QListWidget,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QApplication,
    QMainWindow,
    QSizePolicy,
    QGridLayout,
    QShortcut
    
)
from PyQt5.QtCore import QUrl, pyqtSignal, Qt, QSize, QRect
from PyQt5.QtMultimedia import QSoundEffect
import sys
from utils.utils import parametro


class VentanaInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana inicio")
        self.move(0, 0)
        self.setFixedSize(
            parametro("ventana_inicio_size"),
            parametro("ventana_inicio_size"),
        )

        main_layout = QVBoxLayout()
        background = QLabel(self)
        background.setPixmap(
            QPixmap(parametro("path_fondo_inicio")).scaled(self.width(), self.height())
        )
        background.setGeometry(0, 0, self.width(), self.height())
        label_sala_espera = QLabel("SALA DE ESPERA", self)
        label_sala_espera.setAlignment(Qt.AlignHCenter)  # type: ignore
        label_sala_espera.setFont(QFont("Arial", 30, weight=QFont.Bold))
        main_layout.addWidget(label_sala_espera)
        self.players_layout = QHBoxLayout()
        main_layout.addLayout(self.players_layout)
        self.btn_comenzar = QPushButton("Comenzar", self)
        self.btn_salir = QPushButton("Salir", self)
        main_layout.addWidget(self.btn_comenzar)
        main_layout.addWidget(self.btn_salir)
        self.setLayout(main_layout)
        self.usuarios = {}

    def mostrar_alerta(self, mensaje: str):
        alerta = QMessageBox(self)
        alerta.setWindowTitle("Alerta")
        alerta.setIcon(QMessageBox.Warning)
        alerta.setText(mensaje)
        alerta.setStandardButtons(QMessageBox.Ok)
        alerta.exec()

    def agregar_usuario(self, id: str) -> None:
        print("Agregando label usuario")
        layout = QVBoxLayout()
        label_usuario = QLabel(self)
        label_usuario.setPixmap(QPixmap(parametro("PATH_USER_IMAGE")).scaled(100, 100, transformMode=Qt.TransformationMode.SmoothTransformation))
        label_id = QLabel(id, self)
        layout.addWidget(label_usuario)
        layout.addWidget(label_id)
        self.usuarios[id] = layout
        self.players_layout.addLayout(layout)

    def eliminar_usuario(self, id: str):
        print("Eliminando label usuario")
        self.players_layout.removeItem(self.usuarios[id])
        self.usuarios[id].deleteLater()
        del self.usuarios[id]

    def servidor_cerrado(self, mensaje: str) -> None:
        self.mostrar_alerta(mensaje)
        exit()


class LabelTextos(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = QFont("Arial", 10)
        font.setBold(True)
        self.setFont(font)
        self.setStyleSheet("color: white")
        self.setAlignment(Qt.AlignHCenter)


class LabelCuadrados(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = QFont("Arial", 8)
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)
        self.setStyleSheet("background-color: white")
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(QSize(50, 50))
        self.setMaximumSize(QSize(50, 50))


class CustomButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("background-color: white")


class LabelUserImage(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPixmap(
            QPixmap(parametro("PATH_USER_IMAGE")).scaled(
                80, 80, transformMode=Qt.TransformationMode.SmoothTransformation
            )
        )
        self.setMinimumSize(QSize(80, 80))
        self.setMaximumSize(QSize(80, 80))


class Jugador(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lbl_vidas = LabelCuadrados(str(parametro("NUMERO_VIDAS")), self)
        self.lbl_imagen = LabelUserImage(self)
        self.dado1 = LabelCuadrados("Dado 1", self)
        self.dado2 = LabelCuadrados("Dado 2", self)
        self.lbl_nombre = LabelTextos("Jugador", self)

    def actualizar_dados(self, dados):
        dado1, dado2 = dados
        self.dado1.setText("")
        self.dado2.setText("")
        self.dado1.setStyleSheet("")
        self.dado2.setStyleSheet("")
        self.dado1.setPixmap(QPixmap(parametro("PATH_DADOS")[dado1 - 1]).scaled(self.dado1.width(), self.dado1.height()))
        self.dado2.setPixmap(QPixmap(parametro("PATH_DADOS")[dado2 - 1]).scaled(self.dado1.width(), self.dado1.height()))


class Jugador1(Jugador):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(550, 500, 140, 180)
        vbox = QVBoxLayout(self)
        layout_dados = QHBoxLayout()
        layout_dados.addWidget(self.dado1)
        layout_dados.addWidget(self.dado2)
        hbox = QHBoxLayout()
        hbox.setSpacing(50)
        hbox.addWidget(self.lbl_imagen)
        hbox.addWidget(self.lbl_vidas)
        vbox.addLayout(layout_dados)
        vbox.addLayout(hbox)
        vbox.addWidget(self.lbl_nombre)


class Jugador2(Jugador):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(830, 310, 210, 130)
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        layout_dados = QVBoxLayout()
        layout_dados.setSpacing(15)
        layout_dados.addWidget(self.dado1)
        layout_dados.addWidget(self.dado2)
        hbox.addLayout(layout_dados)
        hbox.addWidget(self.lbl_imagen)
        hbox.addWidget(self.lbl_vidas)
        vbox.addLayout(hbox)
        vbox.addWidget(self.lbl_nombre)


class Jugador3(Jugador):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(550, 120, 140, 180)
        vbox = QVBoxLayout(self)
        layout_dados = QHBoxLayout()
        layout_dados.addWidget(self.dado1)
        layout_dados.addWidget(self.dado2)
        hbox = QHBoxLayout()
        hbox.setSpacing(50)
        hbox.addWidget(self.lbl_imagen)
        hbox.addWidget(self.lbl_vidas)
        vbox.addLayout(hbox)
        vbox.addWidget(self.lbl_nombre)
        vbox.addLayout(layout_dados)


class Jugador4(Jugador):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(200, 310, 210, 130)
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        hbox.addWidget(self.lbl_vidas)
        hbox.addWidget(self.lbl_imagen)
        layout_dados = QVBoxLayout()
        layout_dados.setSpacing(15)
        layout_dados.addWidget(self.dado1)
        layout_dados.addWidget(self.dado2)
        hbox.addLayout(layout_dados)
        vbox.addLayout(hbox)
        vbox.addWidget(self.lbl_nombre)


class VentanaJuego(QWidget):
    senal_env_anunciar_valor = pyqtSignal(str)
    senal_keys_pressed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana juego")
        self.move(0, 0)
        self.setFixedSize(
            parametro("VENTANA_JUEGO_ANCHO"),
            parametro("VENTANA_JUEGO_ALTO"),
        )
        background = QLabel(self)
        background.setPixmap(
            QPixmap(
                parametro("PATH_FONDO_JUEGO")).scaled(self.width(), self.height(), transformMode=Qt.TransformationMode.SmoothTransformation)
        )
        background.setGeometry(0, 0, self.width(), self.height())

        self.jugador_actual = None
        self.label_turno_actual = LabelTextos(f"Turno de {self.jugador_actual}", self)
        self.label_turno_actual.setGeometry(490, 6, 300, 16)

        widget_info = QWidget(self)
        layout_info = QHBoxLayout(widget_info)
        widget_info.setLayout(layout_info)
        widget_info.setGeometry(QRect(0, 34, self.width(), 40))
        self.label_mayor_numero = LabelTextos("Numero mayor anunciado: 0", widget_info)
        layout_info.addWidget(self.label_mayor_numero)
        self.label_turno_anterior = LabelTextos(
            "Turno anterior fue -", widget_info
        )
        layout_info.addWidget(self.label_turno_anterior)
        self.label_numero_turno = LabelTextos("Numero Turno: 1", widget_info)
        layout_info.addWidget(self.label_numero_turno)

        widget_acciones = QWidget(self)
        layout_acciones = QGridLayout(widget_acciones)
        widget_acciones.setGeometry(1020, 580, 200, 100)
        self.btn_anunciar_valor = CustomButton("Anunciar valor", widget_acciones)
        layout_acciones.addWidget(self.btn_anunciar_valor, 0, 0)
        self.txt_valor = QLineEdit(widget_acciones)
        layout_acciones.addWidget(self.txt_valor, 0, 1)
        self.btn_pasar = CustomButton("Pasar turno", widget_acciones)
        layout_acciones.addWidget(self.btn_pasar, 1, 0)
        self.btn_cambiar_dados = CustomButton("Cambiar dados", widget_acciones)
        layout_acciones.addWidget(self.btn_cambiar_dados)
        self.btn_usar_poder = CustomButton("Usar poder", widget_acciones)
        layout_acciones.addWidget(self.btn_usar_poder, 2, 0)
        self.btn_dudar = CustomButton("Dudar", widget_acciones)
        layout_acciones.addWidget(self.btn_dudar, 2, 1)
        self.jugadores = {}

    def iniciar(self, jugadores):
        jugador1 = Jugador1(self)
        jugador2 = Jugador2(self)
        jugador3 = Jugador3(self)
        jugador4 = Jugador4(self)
        id1, id2, id3, id4 = jugadores
        jugador1.lbl_nombre.setText(id1)
        jugador2.lbl_nombre.setText(id2)
        jugador3.lbl_nombre.setText(id3)
        jugador4.lbl_nombre.setText(id4)
        self.jugadores[id1] = jugador1
        self.jugadores[id2] = jugador2
        self.jugadores[id3] = jugador3
        self.jugadores[id4] = jugador4
        self.label_turno_actual.setText(f"Turno de {id1}")
        self.show()

    def actualizar_dados(self, data):
        id, dados = data
        self.jugadores[id].actualizar_dados(dados)

    def enviar_anunciar_valor(self):
        print("Anunciando valor: front")
        self.senal_env_anunciar_valor.emit(self.txt_valor.text())

    def actualizar_numero_mayor(self, numero):
        self.label_mayor_numero.setText(f"Numero mayor anunciado: {numero}")

    def actualizar_turnos(self, turnos):
        id_actual, id_anterior, total = turnos
        self.label_turno_actual.setText(f"Turno de {id_actual}")
        self.label_turno_anterior.setText(f"Turno anterior fue {id_anterior}")
        self.label_numero_turno.setText(f"Numero turno {total}")

    def mostrar_dados(self, data):
        for i in range(len(data)):
            self.actualizar_dados(data)
            
    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.senal_keys_pressed.emit(event.key())


if __name__ == "__main__":

    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    sys.__excepthook__ = hook

    app = QApplication([])
    game = VentanaJuego()
    game.show()

    sys.exit(app.exec())



if __name__ == "__main__":

    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    sys.__excepthook__ = hook

    app = QApplication([])
    game = VentanaJuego()
    game.show()

    sys.exit(app.exec())
