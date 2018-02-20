from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Plot(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.habitacion = QComboBox()
        self.nombreAlarma = QComboBox()
        self.hora = QComboBox()
        self.minutos = QComboBox()
        self.setitup = QSplitter()
        self.setitup.addWidget()

        self.grid = QGridLayout()
        self.grid.setRowMinimumHeight(0, 350)
        self.grid.setRowMinimumHeight(0, 50)
