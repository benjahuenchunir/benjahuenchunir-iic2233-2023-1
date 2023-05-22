from PyQt5.QtGui import QPixmap, QFont, QMouseEvent
import parametros as p
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QAbstractItemView, QStackedWidget, QWidget, QListWidget, QApplication, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QComboBox
from PyQt5.QtCore import QUrl, pyqtSignal, QTimer, QPropertyAnimation, QPoint, Qt, QSize
from PyQt5.QtMultimedia import QSoundEffect
import sys
from collections import defaultdict
import os


class VentanaInicio(QWidget):

    senal_login = pyqtSignal(str, object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana inicio")
        self.move(0, 0)
        vbox = QVBoxLayout()

        background = QLabel(self)
        background.setPixmap(QPixmap(p.PATH_FONDO))
        self.logo = QLabel(self)
        self.logo.setGeometry(40, 50, 550, 100)
        self.logo.setPixmap(QPixmap(p.PATH_LOGO))
        self.logo.setScaledContents(True)
        vbox.addWidget(background)

        hbox = QHBoxLayout()
        self.label_username = QLabel("Usuario", self)
        self.txt_username = QLineEdit("", self)
        hbox.addWidget(self.label_username)
        hbox.addWidget(self.txt_username)
        self.dropdown_menu = QComboBox()
        self.dropdown_menu.addItem(p.MODO_CONSTRUCTOR)
        self.btn_login = QPushButton("Login", self)
        self.btn_exit = QPushButton("Salir", self)
        self.btn_exit.clicked.connect(self.close)
        vbox.addLayout(hbox)
        vbox.addWidget(self.dropdown_menu)
        vbox.addWidget(self.btn_login)
        vbox.addWidget(self.btn_exit)

        self.setLayout(vbox)
        self.btn_login.clicked.connect(self.login)

    def cargar_mapas(self, mapas):
        for nombre, mapa in mapas:
            self.dropdown_menu.addItem(nombre, mapa)
        self.show()

    def login(self):
        print(self.txt_username.text())
        indice_seleccion = self.dropdown_menu.currentIndex()
        self.senal_login.emit(
            self.txt_username.text(),
            self.dropdown_menu.itemData(indice_seleccion))

    def alerta_nombre_invalido(self, razon):
        alerta = QMessageBox(self)
        alerta.setWindowTitle("Nombre inválido")
        alerta.setIcon(QMessageBox.Warning)
        alerta.setText(razon)
        alerta.setStandardButtons(QMessageBox.Ok)
        alerta.exec()


class ElementoConstructor(QWidget):
    def __init__(self, path_imagen, cantidad):
        super().__init__()

        hbox = QHBoxLayout(self)
        self.setLayout(hbox)

        self.label_elemento = QLabel(self)
        self.label_elemento.setPixmap(QPixmap(path_imagen).scaled(64, 64, Qt.KeepAspectRatio) )
        hbox.addWidget(self.label_elemento)

        self.label_cantidad = QLabel(cantidad, self)
        self.label_cantidad.setFont(QFont('Arial', 16))
        hbox.addWidget(self.label_cantidad)

    def actualizar_cantidad(self, cantidad):
        self.label_cantidad.setText(cantidad)


class MapaJuego(QWidget):
    senal_on_click = pyqtSignal(int, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.mapa = QGridLayout(self)
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
        self.senal_on_click.emit(event.x(), event.y())

    def colocar_elemento(self, elemento, fil, col):
        label = QLabel(self)
        label.setPixmap(QPixmap(p.FILTROS[p.FILTRO_TODOS][elemento]).scaled(p.TAMANO_GRILLA, p.TAMANO_GRILLA))
        self.mapa.addWidget(label, fil, col)


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
            self.lista_elementos.setItemWidget(item1, ElementoConstructor(nombre_archivo, str(p.MAXIMO_ELEMENTOS[nombre_mapa])))

    def actualizar_cantidad_elemento(self, elemento, cantidad):
        for i in range(self.lista_elementos.count()):
            item = self.lista_elementos.item(i)
            if item.whatsThis() == elemento:
                self.lista_elementos.itemWidget(item).actualizar_cantidad(cantidad)


class MenuJuego(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        layout_timer = QHBoxLayout()
        layout_timer.addWidget(QLabel("Tiempo", self))
        self.label_timer = QLabel(self)
        layout_timer.addWidget(self.label_timer)
        vbox.addLayout(layout_timer)

        layout_vidas = QHBoxLayout()
        layout_vidas.addWidget(QLabel("Vidas", self))
        self.label_vidas = QLabel(str(p.CANTIDAD_VIDAS - 1), self)
        layout_vidas.addWidget(self.label_vidas)
        vbox.addLayout(layout_vidas)

        self.btn_pausar = QPushButton('Pausar')
        vbox.addWidget(self.btn_pausar)

    def actualizar_tiempo(self, tiempo):
        self.label_timer.setText(tiempo)

    def actualizar_vidas(self, vidas):
        self.label_vidas.setText(vidas)


class VentanaJuego(QWidget):
    senal_mover_personaje = pyqtSignal(int)
    senal_eliminar_villanos = pyqtSignal()
    senal_godmode = pyqtSignal()
    senal_liberar_aossa = pyqtSignal()

    def __init__(self, senal_pausar) -> None:
        super().__init__()
        self.mapa = MapaJuego()
        self.setLayout(self.mapa.mapa)
        self.setFixedSize(p.ANCHO_GRILLA * p.TAMANO_GRILLA, p.LARGO_GRILLA * p.TAMANO_GRILLA)
        self.fantasmas = {}
        self.elementos = []
        self.pressed_keys = set()
        self.senal_pausar = senal_pausar

    def iniciar(self):
        self.show()

    def crear_luigi(self, x, y):
        self.label_luigi = Luigi(x, y, self)
        self.label_luigi.show()

    def crear_fantasma(self, id, tipo, nombre_direccion, x, y):
        label_fantasma = Fantasma(tipo, nombre_direccion, x, y, self)
        self.fantasmas[id] = label_fantasma
        label_fantasma.show()

    def crear_elemento(self, tipo, col, fil):
        elemento = QLabel(self)
        elemento.setPixmap(QPixmap(p.SPRITES_ELEMENTOS[tipo]).scaled(p.TAMANO_GRILLA, p.TAMANO_GRILLA))
        self.mapa.mapa.addWidget(elemento, fil, col)
        self.elementos.append(elemento)

    def mover_fantasmas(self, id, *args):
        self.fantasmas[id].mover(*args)

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        self.pressed_keys.add(event.key())
        if event.key() == Qt.Key_P:
            self.senal_pausar.emit()
        if event.key() == Qt.Key_G:
            self.senal_liberar_aossa.emit()
        if len({Qt.Key_K, Qt.Key_I, Qt.Key_L}.intersection(self.pressed_keys)) == 3:
            self.senal_eliminar_villanos.emit()
            self.eliminar_villanos()
        if len({Qt.Key_I, Qt.Key_N, Qt.Key_F}.intersection(self.pressed_keys)) == 3:
            self.senal_godmode.emit()
        if self.label_luigi.current_direction == p.LUIGI_QUIETO:
            key = event.key()
            self.senal_mover_personaje.emit(key)

    def keyReleaseEvent(self, event):
        if event.key() in self.pressed_keys:
            self.pressed_keys.remove(event.key())

    def mover_luigi(self, direccion, pos_final):
        self.label_luigi.mover(direccion, pos_final)

    def eliminar_villanos(self):
        for fantasma in self.fantasmas.values():
            fantasma.hide()
            
    def eliminar_fantasma(self, id):
        self.fantasmas[id].deleteLater()
        del self.fantasmas[id]

    def limpiar_nivel(self):
        self.label_luigi.deleteLater()
        for fantasma in self.fantasmas.values():
            fantasma.deleteLater()
        self.fantasmas.clear()
        for elemento in self.elementos:
            elemento.deleteLater()
        self.elementos.clear()


class VentanaCompleta(QStackedWidget):
    senal_cargar_mapa = pyqtSignal(list)
    senal_colocar_elemento_constructor = pyqtSignal(str, int, int)
    senal_pausar = pyqtSignal()
    senal_reiniciar_juego = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(0, 0)

        self.widget_constructor = QWidget()
        self.layout_constructor = QHBoxLayout()
        self.menu_constructor = MenuConstructor(self)
        self.mapa = MapaJuego(self)
        self.layout_constructor.addWidget(self.menu_constructor)
        self.layout_constructor.addWidget(self.mapa)
        self.widget_constructor.setLayout(self.layout_constructor)
        self.addWidget(self.widget_constructor)

        self.widget_juego = QWidget()
        self.layout_juego = QHBoxLayout()
        self.menu_juego = MenuJuego(self)
        self.mapa_juego = VentanaJuego(self.senal_pausar)
        self.mapa_juego.setFocusPolicy(Qt.NoFocus)
        self.layout_juego.addWidget(self.menu_juego)
        self.layout_juego.addWidget(self.mapa_juego)
        self.widget_juego.setLayout(self.layout_juego)
        self.addWidget(self.widget_juego)

    def cargar_mapa_constructor(self):
        self.senal_cargar_mapa.emit(self.mapa.mapa_lista)

    def jugar(self):
        self.setCurrentWidget(self.widget_juego)
        self.mapa_juego.setFocus()

    def emitir_colocar_elemento(self, x, y):
        elemento_seleccionado = self.menu_constructor.lista_elementos.selectedItems()[0].whatsThis()
        self.senal_colocar_elemento_constructor.emit(elemento_seleccionado, x, y)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_P:
            self.senal_pausar.emit()

    def pausar(self, is_focused):
        if is_focused:
            self.mapa_juego.clearFocus()
        else:
            self.mapa_juego.setFocus()

    def terminar_partida(self, resultado, path_audio, nombre_usuario, puntaje):
        sonido = QSoundEffect()
        sonido_url = QUrl.fromLocalFile(path_audio)
        sonido.setSource(sonido_url)
        sonido.play()
        self.mostrar_mensaje(resultado, nombre_usuario, puntaje)

    def mostrar_mensaje(self, resultado, nombre_usuario, score):
        mensaje = QMessageBox(self)
        mensaje.setWindowTitle(resultado)
        mensaje.setText(f"Usuario: {nombre_usuario}\nPuntuación: {score}")
        btn_salir = mensaje.addButton("Salir", QMessageBox.RejectRole)
        btn_reiniciar = mensaje.addButton("Jugar de nuevo", QMessageBox.NoRole)
        mensaje.exec_()
        if mensaje.clickedButton() == btn_salir:
            self.close()
        elif mensaje.clickedButton() == btn_reiniciar:
            self.senal_reiniciar_juego.emit()
            self.mapa_juego.setFocus()


if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaCompleta()
    ventana.show()
    sys.exit(app.exec())
