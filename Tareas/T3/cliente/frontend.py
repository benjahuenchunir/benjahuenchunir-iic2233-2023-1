from PyQt5.QtGui import QPixmap, QMouseEvent
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
)
from PyQt5.QtCore import QUrl, pyqtSignal, Qt, QSize
from PyQt5.QtMultimedia import QSoundEffect
import sys


class VentanaInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana inicio")
        self.move(0, 0)

        main_layout = QVBoxLayout()
        
        
        background = QLabel(self)
        background.setPixmap(QPixmap("sprites/background/background_inicio.png"))
        # Importante el QLabel sea transparente a los eventos del mouse.
        background.setScaledContents(True)
        background.setGeometry(0, 0, 800, 500)

        main_layout.addWidget(background)
        main_layout.addWidget(QLabel("SALA DE ESPERA", self))
        players_layout = QHBoxLayout()
        main_layout.addLayout(players_layout)
        self.btn_comenzar = QPushButton("Comenzar", self)
        self.btn_salir = QPushButton("Salir", self)
        main_layout.addWidget(self.btn_comenzar)
        main_layout.addWidget(self.btn_salir)

        self.setLayout(main_layout)
        
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana inicio")
        self.move(0, 0)
        vbox = QVBoxLayout()

        background = QLabel(self)
        background.setPixmap(QPixmap("sprites/background/background_inicio.png"))
        vbox.addWidget(background)

        hbox = QHBoxLayout()
        self.label_username = QLabel("Usuario", self)
        self.txt_username = QLineEdit("", self)
        hbox.addWidget(self.label_username)
        hbox.addWidget(self.txt_username)
        self.dropdown_menu = QComboBox()
        self.btn_login = QPushButton("Login", self)
        self.btn_exit = QPushButton("Salir", self)
        vbox.addLayout(hbox)
        vbox.addWidget(self.dropdown_menu)
        vbox.addWidget(self.btn_login)
        vbox.addWidget(self.btn_exit)

        self.setLayout(vbox)
        

if __name__ == "__main__":

    def hook(type_, value, traceback):
        print(type_)
        print(traceback)

    sys.__excepthook__ = hook

    app = QApplication([])
    game = VentanaInicio()
    game.show()

    sys.exit(app.exec())
