import sys
#import Alertas
from queue import Queue
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Angry Flower Monitoring")
        self.setGeometry(100,100,1200,600)

        self.cw = CentralWidget()
        self.setCentralWidget(self.cw)

        self.bw = BottomWidget()
        self.dw = QDockWidget('Botones')
        self.dw.setFloating(True)
        self.dw.setWidget(self.bw)
        self.dw.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dw)

        self.show()

class CentralWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.llamados = QFrame()
        self.llamados.setFrameShape(QFrame.StyledPanel)
        self.alarmas = QFrame()
        self.alarmas.setFrameShape(QFrame.StyledPanel)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.llamados)
        splitter.addWidget(self.alarmas)
        splitter.setSizes([800,400])

        cw = QHBoxLayout()
        cw.addWidget(splitter)
        self.setLayout(cw)

class BottomWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        btn0 = QPushButton('Cama 0', self)
        btn1 = QPushButton('Cama 1', self)
        btn0_off = QPushButton('Cama 0 off', self)
        btn1_off = QPushButton('Cama 1 off', self)

        botones = QHBoxLayout()
        botones.addWidget(btn0)
        botones.addWidget(btn1)
        botones.addWidget(btn0_off)
        botones.addWidget(btn1_off)
        self.setLayout(botones)

        btn0.clicked.connect(self.boton0)
        btn1.clicked.connect(self.boton1)
        btn0_off.clicked.connect(self.boton0_off)
        btn1_off.clicked.connect(self.boton1_off)

    def boton0(self):
        global QueueCamas
        QueueAtender.put(1)

    def boton1(self):
        global QueueCamas
        QueueAtender.put(2)

    def boton0_off(self):
        global QueueCamas
        QueueCamas.put(1)

    def boton1_off(self):
        global QueueCamas
        QueueCamas.put(2)


if __name__== '__main__':
    QueueAtender = Queue()
    QueueAtendido = Queue()
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
