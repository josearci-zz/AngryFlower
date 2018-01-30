import time
from queue import Queue
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

QueueAtender = Queue()
QueueAtendido = Queue()

class SistemaAlertas(object):
    def __init__(self, parent=None):
        super(SistemaAlertas, self).__init__()
        self.plot = Plot()
        self.manejolistas = ManejoListas()
        self.lista_llamados = []
        self.lista_total = []
        self.tiempo = []

        self.plot.btn0_on.clicked.connect(lambda: self.boton_on(1))
        self.plot.btn1_on.clicked.connect(lambda: self.boton_on(2))
        self.plot.btn2_on.clicked.connect(lambda: self.boton_on(3))
        self.plot.btn0_off.clicked.connect(lambda: self.boton_off(1))
        self.plot.btn1_off.clicked.connect(lambda: self.boton_off(2))
        self.plot.btn2_off.clicked.connect(lambda: self.boton_off(3))

        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizarListaPantalla)
        self.timer.start(1000)

    def procesarSenal(self):
        global QueueAtender
        global QueueAtendido
        # Quitar paciente
        if not QueueAtendido.empty() and len(self.lista_llamados)!=0:
            dato_saliente = QueueAtendido.get()
            apuntador = self.lista_llamados.index(dato_saliente)
            self.tiempo.remove(self.tiempo[apuntador])
            self.lista_llamados.remove(dato_saliente)

        # Poner paciente
        elif not QueueAtender.empty():
            dato_entrante = QueueAtender.get()
            tiempo_inicio = time.time()
            self.tiempo.append(tiempo_inicio)
            self.lista_llamados.append(dato_entrante)

        self.actualizarListaPantalla()

    def calculotiempo(self, apuntador):
        tiempo_actual = time.time()
        tiempo_diferencia = int((tiempo_actual-self.tiempo[apuntador])/1) # poner 60 para minutos
        return tiempo_diferencia

    def actualizarListaPantalla(self): # esta funcion no me gusta puede pasar a ser un apuntador
        for i in range(10):
            if i<len(self.lista_llamados):
                tiempo = self.calculotiempo(i)
                self.plot.update(i,self.manejolistas.quienesesteID(self.lista_llamados[i]),str(tiempo))
            else:
                self.plot.update(i,self.manejolistas.quienesesteID(0)," ")

    def boton_on(self,dato):
        if not self.manejolistas.existe(dato,self.lista_llamados):
            QueueAtender.put(dato)
            self.procesarSenal()

    def boton_off(self,dato):
        if self.manejolistas.existe(dato,self.lista_llamados):
            QueueAtendido.put(dato)
            self.procesarSenal()

class ManejoListas(object):
    def __init__(self):
        self.nombres_camas = [["Habitación","1","a","Luis Felipe"],["Habitación","2","b","José Ricardo"],["Baño","69"," ","Angry Flower"]]

    def update_lista(self):
        pass

    def existe(self, dato, lista):
        if dato in lista:
            return True
        else:
            return False

    def quienesesteID(self, dato):
        if dato == 0:
            paciente = [" "," "," "," "]
        else:
            paciente = self.nombres_camas[dato-1]
        return paciente

class Plot(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.btn0_on = QPushButton('Cama 0 on', self)
        self.btn1_on = QPushButton('Cama 1 on', self)
        self.btn2_on = QPushButton('Baño 69 on', self)
        self.btn0_off = QPushButton('Cama 0 off', self)
        self.btn1_off = QPushButton('Cama 1 off', self)
        self.btn2_off = QPushButton('Baño 69 off', self)

        botones = QHBoxLayout()
        botones.addWidget(self.btn0_on)
        botones.addWidget(self.btn1_on)
        botones.addWidget(self.btn2_on)
        botones.addWidget(self.btn0_off)
        botones.addWidget(self.btn1_off)
        botones.addWidget(self.btn2_off)

        self.grid = QGridLayout()
        self.grid.sizeHint()
        filas = 11
        columnas = [100,50,50,450,150]
        self.label_array = []
        for i in range(filas-1):
            temp = []
            for j in range(len(columnas)):
                temp.append(QLabel())
                #temp[j].setTextFormat
            self.label_array.append(temp)
        for i in range(filas-1):
            for j in range(len(columnas)):
                self.grid.addWidget(self.label_array[i][j],i,j)
        for i in  range(len(columnas)):
            self.grid.setColumnMinimumWidth(i,columnas[i])

        self.grid.addLayout(botones,10,0,1,5)

    def update(self, fila, lista, tiempo):
        self.label_array[fila][0].clear()
        self.label_array[fila][1].clear()
        self.label_array[fila][2].clear()
        self.label_array[fila][3].clear()
        self.label_array[fila][4].clear()
        self.label_array[fila][0].setText(lista[0])
        self.label_array[fila][1].setText(lista[1])
        self.label_array[fila][2].setText(lista[2])
        self.label_array[fila][3].setText(lista[3])
        self.label_array[fila][4].setText(tiempo)
