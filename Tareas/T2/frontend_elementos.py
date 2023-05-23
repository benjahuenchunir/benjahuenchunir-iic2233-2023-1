from PyQt5.QtGui import QPixmap, QFont
import parametros as p
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QGridLayout
from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint, Qt
from collections import defaultdict
import os


class ElementoConstructor(QWidget):
    def __init__(self, path_imagen, cantidad):
        super().__init__()

        hbox = QHBoxLayout(self)
        self.setLayout(hbox)

        self.label_elemento = QLabel(self)
        self.label_elemento.setPixmap(
            QPixmap(path_imagen).scaled(
                p.TAMANO_GRILLA, p.TAMANO_GRILLA, Qt.KeepAspectRatio
            )
        )
        hbox.addWidget(self.label_elemento)

        self.label_cantidad = QLabel(cantidad, self)
        self.label_cantidad.setFont(QFont("Arial", 16))
        hbox.addWidget(self.label_cantidad)

    def actualizar_cantidad(self, cantidad):
        self.label_cantidad.setText(cantidad)


class FondoMapa(QGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.cargar_mapa()

    def cargar_mapa(self):
        for fil in range(p.LARGO_GRILLA):
            for col in range(p.ANCHO_GRILLA):
                if (
                    fil == 0
                    or fil == p.LARGO_GRILLA - 1
                    or col == 0
                    or col == p.ANCHO_GRILLA - 1
                ):
                    borde = QLabel()
                    borde.setPixmap(
                        QPixmap(p.SPRITES_ELEMENTOS[p.MAPA_BORDE]).scaled(
                            p.TAMANO_GRILLA, p.TAMANO_GRILLA
                        )
                    )
                    self.addWidget(borde, fil, col)
                else:
                    fondo = QLabel()
                    fondo.setStyleSheet(
                        f"""
                            background-color: #2D2C2C;
                            border: 2px solid #242323;
                        """
                    )
                    fondo.setFixedSize(p.TAMANO_GRILLA, p.TAMANO_GRILLA)
                    self.addWidget(fondo, fil, col)


class Fantasma(QLabel):
    def __init__(self, tipo, direccion, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imagenes = defaultdict(list)
        self.tipo = tipo
        self.current_direction = direccion
        self.current_image = 0
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(400)
        self.anim.finished.connect(self.parar_movimiento)
        self.timer = QTimer(self)
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.animar)
        self.cargar_imagenes()
        self.setGeometry(x, y, p.TAMANO_GRILLA, p.TAMANO_GRILLA)

    def cargar_imagenes(self):
        for image in os.listdir(p.PATH_ENTIDADES):
            if self.tipo in image:
                self.imagenes[os.path.splitext(image)[0].split("_")[2]].append(
                    QPixmap(os.path.join(p.PATH_ENTIDADES, image)).scaled(
                        p.TAMANO_GRILLA, p.TAMANO_GRILLA, Qt.KeepAspectRatio
                    )
                )
        self.setPixmap(
            self.imagenes[self.current_direction][self.current_image])

    def mover(self, direccion, x, y):
        self.current_direction = direccion
        self.anim.setEndValue(QPoint(x, y))
        self.timer.start()
        self.anim.start()

    def animar(self):
        self.current_image = (self.current_image + 1) % len(
            self.imagenes[self.current_direction]
        )
        self.setPixmap(
            self.imagenes[self.current_direction][self.current_image])

    def parar_movimiento(self):
        self.timer.stop()
        self.animar()


class Roca(QLabel):
    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(400)
        self.setPixmap(
            QPixmap(p.SPRITES_ELEMENTOS[p.MAPA_ROCA]).scaled(
                p.TAMANO_GRILLA, p.TAMANO_GRILLA
            )
        )
        self.setGeometry(x, y, p.TAMANO_GRILLA, p.TAMANO_GRILLA)

    def mover(self, x, y):
        self.anim.setEndValue(QPoint(x, y))
        self.anim.start()


class Luigi(QLabel):
    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images_luigi = defaultdict(list)
        self.current_direction = p.LUIGI_QUIETO
        self.current_image = 0
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(400)
        self.anim.finished.connect(self.parar_movimiento)
        self.timer = QTimer(self)
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.animar_luigi)
        self.cargar_imagenes_luigi()
        self.setGeometry(x, y, p.TAMANO_GRILLA, p.TAMANO_GRILLA)

    def cargar_imagenes_luigi(self):
        for image in os.listdir(p.PATH_ENTIDADES):
            if p.NOMBRE_LUIGI in image:
                self.images_luigi[
                    os.path.splitext(image)[0].split("_")[1]].append(
                    QPixmap(os.path.join(p.PATH_ENTIDADES, image)).scaled(
                        p.TAMANO_GRILLA, p.TAMANO_GRILLA, Qt.KeepAspectRatio
                    )
                )
        self.setPixmap(
            self.images_luigi[self.current_direction][self.current_image])

    def mover(self, direccion, final_pos):
        self.current_direction = direccion
        self.anim.setEndValue(QPoint(*final_pos))
        self.timer.start()
        self.anim.start()

    def animar_luigi(self):
        self.current_image = (self.current_image + 1) % len(
            self.images_luigi[self.current_direction]
        )
        self.setPixmap(
            self.images_luigi[self.current_direction][self.current_image])

    def parar_movimiento(self):
        self.current_direction = p.LUIGI_QUIETO
        self.timer.stop()
        self.animar_luigi()
