import sys
import time
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
    def __init__(self):
        QWidget.__init__(self)

        self.llamados = Llamados()

        self.alarmas = QFrame()
        self.alarmas.setFrameShape(QFrame.StyledPanel)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.llamados)
        splitter.addWidget(self.alarmas)
        splitter.setSizes([800,400])

        cw = QHBoxLayout()
        cw.addWidget(splitter)
        self.setLayout(cw)

class Llamados(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.datos = Informacion()
        self.pacientes = Obtener_pacientes()

        self.numero_plots = 10

        self.grid = QGridLayout()
        for i in range(self.numero_plots):
            self.grid.setRowMinimumHeight(i,60)
        self.setLayout(self.grid)

    def llamados_update(self):
        lista_llamados = self.pacientes.lista()
        conteo = 0
        for i in lista_llamados:
            datos_widget = self.datos.datos_ready(i)
            self.grid.addLayout(datos_widget,conteo,0)
            conteo += 1
"""        for i in range(len(lista_llamados),self.numero_plots):
            datos_widget = self.datos.datos_ready([" "," "," "])
            self.grid.addWidget(datos_widget,conteo,0)
            conteo += 1"""

class Informacion(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # Sectores widget
        self.numero = QLabel()
        self.nombre = QLabel()
        self.tiempo = QLabel()
        self.grid = QGridLayout(self)
        self.grid.setColumnMinimumWidth(0,100)
        self.grid.setColumnMinimumWidth(1,550)
        self.grid.setColumnMinimumWidth(2,150)

    def datos_ready(self, datos):
        self.numero.setText(str(datos[0]))
        self.nombre.setText(datos[1])
        self.tiempo.setText(datos[2])

        self.grid.addWidget(self.numero,0,0)
        self.grid.addWidget(self.nombre,0,1)
        self.grid.addWidget(self.nombre,0,2)
        return self.grid

class Obtener_pacientes(object):
    def __init__(self):
        super(Obtener_pacientes, self).__init__()
        self.pacientes = self.sacar_pacientes()

        # Lista de pacientes para plot
        self.lista_llamados = []

    def sacar_pacientes(self):
        # NOTA: deben estar ordenados por el numero de la cama!g
        nombres_camas = [[1,"Luis Felipe","1 hora"],[2,"Jose Ricardo","1 hora"],[3,"Angry Flower","1 hora"]]
        return nombres_camas

    def lista(self):
        global QueueAtender
        global QueueAtendido

        if not QueueAtender.empty():
            input_on = QueueAtender.get()
            self.lista_llamados.append(self.pacientes[input_on-1])
        elif not QueueAtendido.empty():
            input_off = QueueAtendido.get()
            for i in self.pacientes:
                if i[0] == abs(input_off): #cambiar input
                    self.lista_llamados.remove(i)
                    break

        return self.lista_llamados

class BottomWidget(QWidget): # Cambiar por leer puerto serial
    def __init__(self):
        QWidget.__init__(self)
        self.llw = Llamados()

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
        QueueAtender.put(1)
        self.llw.llamados_update()

    def boton1(self):
        global QueueCamas
        QueueAtender.put(2)
        #self.llw.llamados_update()

    def boton2(self):
        global QueueCamas
        QueueAtender.put(3)
        #self.llw.llamados_update()

    def boton0_off(self):
        global QueueCamas
        QueueCamas.put(-1)
        #self.llw.llamados_update()

    def boton1_off(self):
        global QueueCamas
        QueueCamas.put(-2)
        #self.llw.llamados_update()

    def boton2_off(self):
        global QueueCamas
        QueueCamas.put(-3)
        #self.llw.llamados_update()

if __name__== '__main__':

    QueueCamas = Queue()
    QueueAtender = Queue()
    QueueAtendido = Queue()
    app = QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())


"""
splitter = QSplitter(Qt.Horizontal)
splitter.addWidget(self.numero)
splitter.addWidget(self.nombre)
splitter.addWidget(self.tiempo)
splitter.setSizes([100,500,200])
return splitter
"""
