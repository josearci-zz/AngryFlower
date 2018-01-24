import time
from queue import Queue
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class SistemaAlertas(object):
    def __init__(self):
        self.plot = Plot()
        self.manejolistas = ManejoListas()
        self.lista_llamados = []
        self.tiempo = []

    # Procesar señal
    def __call__(self, QueueAtender, QueueAtendido):
        # Quitar paciente
        if not QueueAtendido.empty() and len(self.lista_llamados)!=0:
            dato_saliente = QueueAtendido.get()
            if self.manejolistas.existe(dato_saliente,self.lista_llamados):
                apuntador = self.lista_llamados.index(dato_saliente)
                self.tiempo.remove(self.tiempo[apuntador])
                self.lista_llamados.remove(dato_saliente)
                self.actualizarListaPantalla()

        # Poner paciente
        elif not QueueAtender.empty():
            dato_entrante = QueueAtender.get()
            if not self.manejolistas.existe(dato_entrante, self.lista_llamados):
                tiempo_inicio = time.time()
                self.tiempo.append(tiempo_inicio)
                self.lista_llamados.append(dato_entrante)
                self.actualizarListaPantalla()

    def calculotiempo(self, apuntador):
        tiempo_actual = time.time()
        tiempo_diferencia = tiempo_actual-self.tiempo[apuntador]
        return tiempo_diferencia

    def actualizarListaPantalla(self): # esta funcion no me gusta puede pasar a ser un apuntador
        for i in range(10):
            if i<len(self.lista_llamados):
                tiempo = self.calculotiempo(i)
                self.plot.update(i,self.manejolistas.quienesesteID(self.lista_llamados[i]),str(tiempo))
            else:
                self.plot.update(i,self.manejolistas.quienesesteID(0)," ")

class ManejoListas(object):
    def __init__(self):
        self.nombres_camas = [["Habitacion","1","Luis Felipe"],["Habitacion","2","Jose Ricardo"],["Baño","69","Angry Flower"]]

    def update_lista(self):
        pass

    def existe(self, dato, lista):
        if dato in lista:
            return True
        else:
            return False

    def quienesesteID(self, dato):
        if dato==0:
            paciente = [" "," "," "]
        else:
            paciente = self.nombres_camas[dato-1]
        return paciente

class Plot(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.grid = QGridLayout()
        filas = [60]*10
        for i in range(len(filas)):
            self.grid.setRowMinimumHeight(i,filas[i])

        #for i in range(10):
        #        self.grid.addWidget(QLabel("B"+str(i)),i,0)

    def update(self, fila, lista, tiempo):
        tipo_label = QLabel()
        numero_label = QLabel()
        nombre_label = QLabel()
        tiempo_label = QLabel()
        grid = QGridLayout()

        columnas = [100,50,550,100]
        for i in range(len(columnas)):
            grid.setColumnMinimumWidth(i,columnas[i])

        tipo_label.setText(lista[0])
        numero_label.setText(lista[1])
        nombre_label.setText(lista[2])
        tiempo_label.setText(tiempo)

        grid.addWidget(tipo_label,0,0)
        grid.addWidget(numero_label,0,1)
        grid.addWidget(nombre_label,0,2)
        grid.addWidget(tiempo_label,0,3)

        return grid
