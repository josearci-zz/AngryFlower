import sys
import numpy as np
from queue import Queue
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # Create stuff
        self.cw = CentralWidget()
        self.setCentralWidget(self.cw)

        # Create Buttons
        self.bw = BottomWidget()
        self.dw = QDockWidget('Botones')
        self.dw.setFloating(True)
        self.dw.setWidget(self.bw)
        self.dw.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dw)

        # Format the main window
        self.setGeometry(100,100,1200,600)
        self.setWindowTitle("Angry Flower Monitoring")

        # Show window
        self.show()

class CentralWidget(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.list = []
        self.conteo = 0
        self.numero = QLabel()
        self.nombre = QLabel()
        self.tiempo = QLabel()

        self.camas = QSplitter(Qt.Vertical)
        self.camas.setSizes([60]*10)

        self.alarmas = QFrame()
        self.alarmas.setFrameShape(QFrame.StyledPanel)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.camas)
        splitter.addWidget(self.alarmas)
        splitter.setSizes([800,400])

        cw = QHBoxLayout()
        cw.addWidget(splitter)
        self.setLayout(cw)

    def LLamadoCama(self):
        global QueueCamas
        pacientes = [[10,'Luis Felipe Ordoñez'],[15,'José Ricardo Arciniegas'],[99,'Angry Flower']]

        if self.conteo < 10:
            data = QueueCamas.get()
            if data > 0:
                self.conteo += 1
                self.list.append(data)
            else:
                self.conteo -= 1
                self.list.remove(self.list[0]) #solucionar problema de eliminar el correcto

            datos = QSplitter(Qt.Horizontal)

            for i in reversed(self.list):
                self.numero.setText(str(pacientes[i-1][0]))
                self.nombre.setText(pacientes[i-1][1])
                datos.addWidget(self.numero)
                datos.addWidget(self.nombre)
                self.camas.addWidget(datos)
            camaswidget = QVBoxLayout()
            camaswidget.addWidget(self.camas)
            self.setLayout(camaswidget)

class BottomWidget(QWidget): # Cambiar por leer puerto serial
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.cw = CentralWidget()

        btn0 = QPushButton('Cama 0', self)
        btn1 = QPushButton('Cama 1', self)
        btn2 = QPushButton('Cama 2', self)
        btn0_off = QPushButton('Cama 0 off', self)
        btn1_off = QPushButton('Cama 1 off', self)
        btn2_off = QPushButton('Cama 2 off', self)

        botones = QHBoxLayout()
        botones.addWidget(btn0)
        botones.addWidget(btn1)
        botones.addWidget(btn2)
        botones.addWidget(btn0_off)
        botones.addWidget(btn1_off)
        botones.addWidget(btn2_off)
        self.setLayout(botones)

        btn0.clicked.connect(self.boton0)
        btn1.clicked.connect(self.boton1)
        btn2.clicked.connect(self.boton2)
        btn0_off.clicked.connect(self.boton0_off)
        btn1_off.clicked.connect(self.boton1_off)
        btn2_off.clicked.connect(self.boton2_off)

    def boton0(self):
        global QueueCamas
        QueueCamas.put(1)
        self.cw.LLamadoCama()

    def boton1(self):
        global QueueCamas
        QueueCamas.put(2)
        self.cw.LLamadoCama()

    def boton2(self):
        global QueueCamas
        QueueCamas.put(3)
        self.cw.LLamadoCama()

    def boton0_off(self):
        global QueueCamas
        QueueCamas.put(-1)
        self.cw.LLamadoCama()

    def boton1_off(self):
        global QueueCamas
        QueueCamas.put(-2)
        self.cw.LLamadoCama()

    def boton2_off(self):
        global QueueCamas
        QueueCamas.put(-3)
        self.cw.LLamadoCama()

if __name__== '__main__':
    QueueCamas = Queue()
    app = QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())
