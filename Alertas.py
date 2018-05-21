import time
import atexit
#import pygsheets
import ConexionSerial
from queue import Queue
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#from oauth2client.service_account import ServiceAccountCredentials

QueueAtender = Queue()
QueueAtendido = Queue()

class SistemaAlertas(object):
    def __init__(self, parent=None):
        super(SistemaAlertas, self).__init__()
        self.plot = Plot()
        self.manejolistas = ManejoListas()
        self.conexion = ConexionSerial.ReadSerial()
        self.lista_llamados = []
        self.lista_total = []
        self.tiempo = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.procesarSenal)
        self.timer.start(50)

        atexit.register(self.conexion.cerrar_puerto)

    def procesarSenal(self):
        global QueueAtender
        global QueueAtendido

        # Leer Serial
        inc_value = self.conexion.read()

        if inc_value < 0:
            self.llamado_off(abs(inc_value))
            # Quitar paciente
            if not QueueAtendido.empty() and len(self.lista_llamados)!=0:
                dato_saliente = QueueAtendido.get()
                apuntador = self.lista_llamados.index(dato_saliente)
                self.tiempo.remove(self.tiempo[apuntador])
                self.lista_llamados.remove(dato_saliente)

        if inc_value > 0:
            self.llamado_on(inc_value)
            # Poner paciente
            if not QueueAtender.empty():
                dato_entrante = QueueAtender.get()
                tiempo_inicio = time.time()
                self.tiempo.append(tiempo_inicio)
                self.lista_llamados.append(dato_entrante)

        self.actualizarListaPantalla()

    def calculotiempo(self, apuntador):
        tiempo_actual = time.time()
        tiempo_diferencia = int((tiempo_actual-self.tiempo[apuntador])/60) # poner 60 para minutos
        linea = int(tiempo_diferencia/(5))
        puntos = tiempo_diferencia%5
        texto_tiempo = ("|"*linea)+("."*puntos)
        return texto_tiempo

    def actualizarListaPantalla(self): # esta funcion no me gusta puede pasar a ser un apuntador
        for i in range(10):
            if i<len(self.lista_llamados):
                tiempo = self.calculotiempo(i)
                self.plot.update(i,self.manejolistas.quienesesteID(self.lista_llamados[i]),tiempo)
            else:
                self.plot.update(i,self.manejolistas.quienesesteID(0)," ")

    def llamado_on(self,dato):
        if not self.manejolistas.existe(dato,self.lista_llamados):
            QueueAtender.put(dato)

    def llamado_off(self,dato):
        if self.manejolistas.existe(dato,self.lista_llamados):
            QueueAtendido.put(dato)

class ManejoListas(object):
    def __init__(self):
        #self.gc = pygsheets.authorize(outh_file='San Luis-61efa7ccd382.json')
        #self.sheet = self.gc.open("Lista San Luis").sheet1
        #print(self.sheet)
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

        self.grid = QGridLayout()
        self.grid.sizeHint()
        filas = 10
        columnas = [100,50,50,450,150]
        self.label_array = []
        for i in range(filas):
            temp = []
            for j in range(len(columnas)):
                temp_label = QLabel()
                newfont = QFont("Times",15)
                temp_label.setFont(newfont)
                temp.append(temp_label)
            self.label_array.append(temp)
        for i in range(filas):
            for j in range(len(columnas)):
                self.grid.addWidget(self.label_array[i][j],i,j)
        for i in  range(len(columnas)):
            self.grid.setColumnMinimumWidth(i,columnas[i])

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
