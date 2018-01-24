import sys
import Alertas
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

        llamados = Alertas.Plot(self)

        alarmas = QFrame()
        alarmas.setFrameShape(QFrame.StyledPanel)

        splitter = QGridLayout()
        splitter.addLayout(llamados.grid,0,0)
        splitter.addWidget(alarmas,0,1)
        splitter.setColumnMinimumWidth(0,800)
        splitter.setColumnMinimumWidth(1,400)

        self.setLayout(splitter)

class BottomWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        global QueueAtender
        global QueueAtendido

        btn0_on = QPushButton('Cama 0 on', self)
        btn1_on = QPushButton('Cama 1 on', self)
        btn2_on = QPushButton('Baño 69 on', self)
        btn0_off = QPushButton('Cama 0 off', self)
        btn1_off = QPushButton('Cama 1 off', self)
        btn2_off = QPushButton('Baño 69 off', self)

        botones = QHBoxLayout()
        botones.addWidget(btn0_on)
        botones.addWidget(btn1_on)
        botones.addWidget(btn2_on)
        botones.addWidget(btn0_off)
        botones.addWidget(btn1_off)
        botones.addWidget(btn2_off)
        self.setLayout(botones)

        btn0_on.clicked.connect(self.boton0_on)
        btn1_on.clicked.connect(self.boton1_on)
        btn2_on.clicked.connect(self.boton2_on)
        btn0_off.clicked.connect(self.boton0_off)
        btn1_off.clicked.connect(self.boton1_off)
        btn2_off.clicked.connect(self.boton2_off)

        self.enviarsenal = Alertas.SistemaAlertas()

    def boton0_on(self):
        cb_id = 1
        QueueAtender.put(cb_id)
        self.enviarsenal(QueueAtender,QueueAtendido)

    def boton1_on(self):
        cb_id = 2
        QueueAtender.put(cb_id)
        self.enviarsenal(QueueAtender,QueueAtendido)

    def boton2_on(self):
        cb_id = 3
        QueueAtender.put(cb_id)
        self.enviarsenal(QueueAtender,QueueAtendido)

    def boton0_off(self):
        cb_id = 1
        QueueAtendido.put(cb_id)
        self.enviarsenal(QueueAtender,QueueAtendido)

    def boton1_off(self):
        cb_id = 2
        QueueAtendido.put(cb_id)
        self.enviarsenal(QueueAtender,QueueAtendido)

    def boton2_off(self):
        cb_id = 3
        QueueAtendido.put(cb_id)
        self.enviarsenal(QueueAtender,QueueAtendido)

if __name__== '__main__':
    QueueAtender = Queue()
    QueueAtendido = Queue()
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
