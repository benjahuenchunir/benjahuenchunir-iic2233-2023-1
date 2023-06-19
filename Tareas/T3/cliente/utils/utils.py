import json
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
    QGridLayout,
    QSpacerItem,
)
from PyQt5.QtCore import QUrl, pyqtSignal, Qt, QSize, QRect
from PyQt5.QtMultimedia import QSoundEffect
import sys


def parametro(llave: str):
    with open("parametros.json", "rt", encoding="utf-8") as f:
        return json.loads(f.read())[llave]


class Mensaje:
    def __init__(self, operacion=None, data=None):
        self.operacion = operacion
        self.data = data

    def __repr__(self):
        return f"{self.operacion}: {self.data}"

    def __eq__(self, obj):
        return self.operacion == obj
