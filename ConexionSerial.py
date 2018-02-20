import serial

class ReadSerial(object):
    def __init__(self):
        super(ReadSerial, self).__init__()
        #self.ser = serial.Serial('/dev/ttyUSB0',baudrate=9600)
        self.ser = serial.Serial(port='COM4', baudrate=9600, timeout=0)

    def read(self):
        read_serial = self.ser.readline()
        cuarto_bano = read_serial.decode('utf-8')
        if len(cuarto_bano)==0:
            return (0)
        else:
            return (int(cuarto_bano))

    def cerrar_puerto(self):
        self.ser.close()
        print("Puerto cerrado!")
