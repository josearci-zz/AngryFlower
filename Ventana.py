import sys
import Reloj
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

        self.show()

class CentralWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.llamados = Alertas.SistemaAlertas(self)
        self.reloj = Reloj.DigitalClock(self)

        alarmas = QFrame()
        alarmas.setFrameShape(QFrame.StyledPanel)

        grid = QGridLayout()
        grid.addLayout(self.llamados.plot.grid,0,0,3,2)
        grid.addWidget(alarmas,0,2,2,1)
        grid.addWidget(self.reloj,2,2,1,1)

        self.setLayout(grid)

if __name__== '__main__':
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
