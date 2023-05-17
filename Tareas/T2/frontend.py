from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QIcon, QFont, QKeySequence, QDrag, QMouseEvent
import parametros as p
from PyQt5.QtWidgets import QListWidgetItem, QAbstractItemView, QWidget, QShortcut, QListWidget, QMainWindow, QApplication, QStackedLayout, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QComboBox
from PyQt5.QtCore import pyqtSignal, QTimer, QPropertyAnimation, QPoint, Qt, QSize, QByteArray, QDataStream, QIODevice, QMimeData
import sys
from collections import defaultdict
import os


class VentanaInicio(QWidget):

    senal_iniciar_juego = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        #self.setFixedSize(p.ANCHO_GRILLA*100, p.ANCHO_GRILLA*100)
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("sprites/Fondos/fondo_inicio.png"))
        self.background.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.background.setGeometry(0, 0, 1000, 800)
        self.background.setScaledContents(True)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.label_username = QLabel("Usuario", self)
        self.txt_username = QLineEdit("", self)
        self.dropdown_menu = QComboBox()
        self.dropdown_menu.addItem("Opción 1")
        self.btn_login = QPushButton("Login", self)
        hbox.addWidget(self.label_username)
        hbox.addWidget(self.txt_username)
        vbox.addLayout(hbox)
        vbox.addWidget(self.dropdown_menu)
        vbox.addWidget(self.btn_login)
        self.setLayout(vbox)
        self.btn_login.clicked.connect(self.login)
        self.setStyleSheet("background-image: 'sprites/Fondos/fondo_inicio.png'")

    def login(self):
        print(self.txt_username.text())
        self.senal_iniciar_juego.emit(self.txt_username.text())


class ElementoConstructor(QWidget):
    def __init__(self, path_imagen, cantidad):
        super().__init__()

        hbox = QHBoxLayout(self)
        self.setLayout(hbox)

        self.label_elemento = QLabel(self)
        self.label_elemento.setPixmap(QPixmap(path_imagen).scaled(64, 64, Qt.KeepAspectRatio) )
        hbox.addWidget(self.label_elemento)

        self.label_cantidad = QLabel(f'({cantidad})', self)
        self.label_cantidad.setFont(QFont('Arial', 16))
        hbox.addWidget(self.label_cantidad)


class MapaJuego(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.mapa = QGridLayout(self)
        self.mapa_lista = [['-' for i in range(p.ANCHO_GRILLA)] for i in range(p.LARGO_GRILLA)]
        self.elemento_seleccionado = None
        self.elementos_por_poner = p.MAXIMO_ELEMENTOS # TODO otra manera de manejar esto es con el label del list_wdget
        self.mapa.setSpacing(0)
        self.mapa.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mapa)
        for fil in range(p.LARGO_GRILLA):
            for col in range(p.ANCHO_GRILLA):
                if fil == 0 or fil == p.LARGO_GRILLA - 1 or col == 0 or col == p.ANCHO_GRILLA - 1:
                    borde = QLabel(self)
                    borde.setPixmap(QPixmap(p.SPRITES_ELEMENTOS[p.MAPA_BORDE]).scaled(p.TAMANO_GRILLA, p.TAMANO_GRILLA))
                    self.mapa.addWidget(borde, fil, col)
                else:
                    fondo = QLabel(self)
                    fondo.setStyleSheet(f"""
                            background-color: #2D2C2C;
                            border: 2px solid #242323;
                        """)
                    fondo.setFixedSize(p.TAMANO_GRILLA, p.TAMANO_GRILLA)
                    self.mapa.addWidget(fondo, fil, col)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.elemento_seleccionado and self.elementos_por_poner[self.elemento_seleccionado]:
            x, y = event.x(), event.y()
            col, fil = x // p.TAMANO_GRILLA, y // p.TAMANO_GRILLA
            if col in (0, p.ANCHO_GRILLA - 1) or y in (0, p.LARGO_GRILLA - 1):
                return
            label = QLabel(self)
            label.setPixmap(QPixmap(p.FILTROS[p.FILTRO_TODOS][self.elemento_seleccionado]).scaled(p.TAMANO_GRILLA, p.TAMANO_GRILLA))
            self.mapa.addWidget(label, fil, col)
            self.elementos_por_poner[self.elemento_seleccionado] -= 1
            self.mapa_lista[fil][col] = self.elemento_seleccionado


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
                self.imagenes[os.path.splitext(image)[0].split('_')[2]].append(QPixmap(os.path.join(p.PATH_ENTIDADES, image)).scaled(p.TAMANO_GRILLA, p.TAMANO_GRILLA, Qt.KeepAspectRatio))
        self.setPixmap(self.imagenes[self.current_direction][self.current_image])

    def mover(self, direccion, x, y):
        self.current_direction = direccion
        self.anim.setEndValue(QPoint(x, y))
        self.timer.start()
        self.anim.start()

    def animar(self):
        self.current_image = (self.current_image + 1) % len(self.imagenes[self.current_direction])
        self.setPixmap(self.imagenes[self.current_direction][self.current_image])

    def parar_movimiento(self):
        self.timer.stop()
        self.animar()


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
                self.images_luigi[os.path.splitext(image)[0].split('_')[1]].append(QPixmap(os.path.join(p.PATH_ENTIDADES, image)).scaled(p.TAMANO_GRILLA, p.TAMANO_GRILLA, Qt.KeepAspectRatio))
        self.setPixmap(self.images_luigi[self.current_direction][self.current_image])

    def mover(self, direccion, final_pos):
        self.current_direction = direccion
        self.anim.setEndValue(QPoint(*final_pos))
        self.timer.start()
        self.anim.start()

    def animar_luigi(self):
        self.current_image = (self.current_image + 1) % len(self.images_luigi[self.current_direction])
        self.setPixmap(self.images_luigi[self.current_direction][self.current_image])

    def parar_movimiento(self):
        self.current_direction = p.LUIGI_QUIETO
        self.timer.stop()
        self.animar_luigi()


class MenuConstructor(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        menu_constructor = QVBoxLayout()
        self.setLayout(menu_constructor)

        self.filtro_elementos = QComboBox()
        self.filtro_elementos.addItems(p.FILTROS)
        self.filtro_elementos.currentTextChanged.connect(self.filtrar_lista)
        menu_constructor.addWidget(self.filtro_elementos)

        self.lista_elementos = QListWidget(self)
        self.lista_elementos.setDragEnabled(True)
        self.lista_elementos.setDragDropMode(QAbstractItemView.DragDrop)
        self.lista_elementos.setDefaultDropAction(Qt.ActionMask)
        self.lista_elementos.setSelectionMode(QAbstractItemView.SingleSelection)
        self.filtrar_lista(self.filtro_elementos.currentText())
        menu_constructor.addWidget(self.lista_elementos)

        layout_botones = QHBoxLayout()
        self.btn_limpiar = QPushButton("Limpiar", self)
        self.btn_jugar = QPushButton("Jugar", self)
        layout_botones.addWidget(self.btn_limpiar)
        layout_botones.addWidget(self.btn_jugar)
        menu_constructor.addLayout(layout_botones)

    def filtrar_lista(self, texto):
        self.lista_elementos.clear()
        for nombre_mapa, nombre_archivo in p.FILTROS[texto].items():
            if p.MAPA_BORDE in p.FILTROS[texto] and nombre_archivo == p.FILTROS[texto][p.MAPA_BORDE]:
                continue
            item1 = QListWidgetItem()
            item1.setWhatsThis(nombre_mapa)
            item1.setSizeHint(QSize(100, 80))
            self.lista_elementos.addItem(item1)
            self.lista_elementos.setItemWidget(item1, ElementoConstructor(nombre_archivo, p.MAXIMO_ELEMENTOS[nombre_mapa]))


class MenuJuego(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        layout_timer = QHBoxLayout()
        layout_timer.addWidget(QLabel("Tiempo", self))
        self.tiempo_restante = p.TIEMPO_JUEGO
        self.label_timer = QLabel(self.formatear_tiempo(self.tiempo_restante), self)
        layout_timer.addWidget(self.label_timer)
        vbox.addLayout(layout_timer)
        self.timer_juego = QTimer(self)
        self.timer_juego.setInterval(1000)
        self.timer_juego.timeout.connect(self.actualizar_tiempo)

        layout_vidas = QHBoxLayout()
        layout_vidas.addWidget(QLabel("Vidas", self))
        layout_vidas.addWidget(QLabel(str(p.CANTIDAD_VIDAS), self))
        vbox.addLayout(layout_vidas)

        btn_pausar = QPushButton()
        vbox.addWidget(btn_pausar)

    def actualizar_tiempo(self):
        self.tiempo_restante -= 1
        self.label_timer.setText(self.formatear_tiempo(self.tiempo_restante))
        if self.tiempo_restante == 0:
            self.timer_juego.stop()
            self.label_timer.setText("Game Over")

    def formatear_tiempo(self, segundos):
        minutos, segundos = divmod(segundos, 60)
        return f"{minutos}:{segundos}"


class VentanaJuego(QWidget):
    senal_mover_personaje = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self.mapa = MapaJuego()
        self.setLayout(self.mapa.mapa)
        self.setFixedSize(p.ANCHO_GRILLA * p.TAMANO_GRILLA, p.LARGO_GRILLA * p.TAMANO_GRILLA)
        self.fantasmas = {}

    def iniciar(self):
        self.show()

    def crear_luigi(self, x, y):
        self.label_luigi = Luigi(x, y, self)
        print(self.label_luigi.pos())
        self.label_luigi.show()

    def crear_fantasma(self, id, tipo, nombre_direccion, x, y):
        label_fantasma = Fantasma(tipo, nombre_direccion, x, y, self)
        self.fantasmas[id] = label_fantasma
        label_fantasma.show()

    def crear_elemento(self, tipo, fil, col):
        elemento = QLabel(self)
        elemento.setPixmap(QPixmap(p.SPRITES_ELEMENTOS[tipo]).scaled(p.TAMANO_GRILLA, p.TAMANO_GRILLA))
        self.mapa.mapa.addWidget(elemento, fil, col)

    def mover_fantasmas(self, id, *args):
        self.fantasmas[id].mover(*args)

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        if self.label_luigi.current_direction == p.LUIGI_QUIETO:
            key = event.key()
            self.senal_mover_personaje.emit(key)

    def mover_luigi(self, direccion, pos_final):
        self.label_luigi.mover(direccion, pos_final)


class VentanaCompleta(QWidget):
    senal_cargar_mapa = pyqtSignal(list)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(0, 0)
        layout_principal = QHBoxLayout()
        self.setLayout(layout_principal)

        self.layout_menus = QStackedLayout()
        layout_principal.addLayout(self.layout_menus)
        self.menu_constructor = MenuConstructor(self)
        self.layout_menus.addWidget(self.menu_constructor)
        self.menu_juego = MenuJuego(self)
        self.layout_menus.addWidget(self.menu_juego)

        self.layout_mapas = QStackedLayout()
        self.mapa = MapaJuego(self)
        self.mapa_juego = VentanaJuego()
        self.layout_mapas.addWidget(self.mapa)
        self.layout_mapas.addWidget(self.mapa_juego)
        layout_principal.addLayout(self.layout_mapas)

        self.menu_constructor.lista_elementos.itemSelectionChanged.connect(self.cambiar_seleccion_elemento)

    def cargar_mapa(self):
        print('Cargando mapa')
        self.senal_cargar_mapa.emit(self.mapa.mapa_lista)

    def jugar(self):
        self.layout_menus.setCurrentWidget(self.menu_juego)
        self.menu_juego.timer_juego.start()
        self.layout_mapas.setCurrentWidget(self.mapa_juego)

    def keyPressEvent(self, event) -> None:
        super().keyPressEvent(event)
        self.mapa_juego.keyPressEvent(event)
        
    def cambiar_seleccion_elemento(self):
        self.mapa.elemento_seleccionado = self.menu_constructor.lista_elementos.selectedItems()[0].whatsThis()


if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaCompleta()
    ventana.show()
    sys.exit(app.exec())
