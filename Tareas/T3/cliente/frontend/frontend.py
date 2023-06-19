from PyQt5.QtGui import QPixmap, QMouseEvent, QFont
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
    QGridLayout
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
        label_usuario.setPixmap(QPixmap(parametro("PATH_USER_IMAGE")).scaled(100, 100))
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
        self.lbl_vidas = LabelCuadrados("vidas", self)
        self.lbl_imagen = LabelUserImage(self)
        self.dado1 = LabelCuadrados("Dado 1", self)
        self.dado2 = LabelCuadrados("Dado 2", self)
        self.lbl_nombre = LabelTextos("Jugador", self)


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
        self.setGeometry(200, 310, 210, 130)
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        hbox.addWidget(self.lbl_vidas)
        hbox.addWidget(self.lbl_imagen)
        layout_dados = QVBoxLayout()
        layout_dados.setSpacing(10)
        layout_dados.addWidget(self.dado1)
        layout_dados.addWidget(self.dado2)
        hbox.addLayout(layout_dados)
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
        self.setGeometry(830, 310, 210, 130)
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        layout_dados = QVBoxLayout()
        layout_dados.setSpacing(10)
        layout_dados.addWidget(self.dado1)
        layout_dados.addWidget(self.dado2)
        hbox.addLayout(layout_dados)
        hbox.addWidget(self.lbl_imagen)
        hbox.addWidget(self.lbl_vidas)
        vbox.addLayout(hbox)
        vbox.addWidget(self.lbl_nombre)


class VentanaJuego(QWidget):
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
            QPixmap(parametro("PATH_FONDO_JUEGO")).scaled(self.width(), self.height())
        )
        background.setGeometry(0, 0, self.width(), self.height())

        self.jugador_actual = None
        self.label_turno_actual = LabelTextos(f"Turno de {self.jugador_actual}", self)
        self.label_turno_actual.setGeometry(490, 6, 300, 16)

        widget_info = QWidget(self)
        layout_info = QHBoxLayout(widget_info)
        widget_info.setLayout(layout_info)
        widget_info.setGeometry(QRect(0, 34, self.width(), 40))
        self.label_mayor_numero = LabelTextos("Numero mayor anunciado: x", widget_info)
        layout_info.addWidget(self.label_mayor_numero)
        self.label_turno_anterior = LabelTextos(
            "Turno anterior fue 'Jugador'", widget_info
        )
        layout_info.addWidget(self.label_turno_anterior)
        self.label_numero_turno = LabelTextos("Numero Turno: x", widget_info)
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

        self.jugador1 = Jugador1(self)
        self.jugador2 = Jugador2(self)
        self.jugador3 = Jugador3(self)
        self.jugador4 = Jugador4(self)


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
