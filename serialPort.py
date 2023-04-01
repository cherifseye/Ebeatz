import serial 
import serial.tools.list_ports as ports 
from sys import platform
import time

class SerialPort():

    def __init__(self, ser=serial.Serial()):
        self.ser = ser

    def __getListPorts__(self):
        if platform == 'win32':
            return [str(port).split(' ')[0] for port in ports.comports()]

        elif platform == 'darwin':
             return [str(port).split(' ')[0] for port in ports.comports() if "usb" in str(port)]

        elif platform == 'linux' or platform == 'linux2':
            return [str(port).split(' ')[0] for port in ports.comports()]
        
    def portIsOpen(self):
        return self.ser.is_open
    
    def __openPort__(self):
        if not self.portIsOpen():
            self.ser.open()

    def __closePort__(self):
        if self.portIsOpen():
            self.ser.close()

    def sendCommand(self, command):
        self.ser.write(command.encode())

    def readline(self):
        data = self.ser.readline().decode('utf-8')
        return data
    

TestSp = SerialPort()
ser = serial.Serial('/dev/ttyACM1', baudrate=9600)
Lum = 0
TestSp.ser = ser
'''
while True:
    TestSp.sendCommand("FREQ\n")
    time.sleep(1)
    print(type(TestSp.readline()))
    cmd_consigne = "CON" + str(Lum) + "\n"
    TestSp.sendCommand(cmd_consigne)
    time.sleep(1)
    Lum += 10
    if Lum > 255:
        break

    ----------------------------------------------
while Lum <=255:
    cmd = "LUM" + str(Lum) + "\n"
    TestSp.sendCommand(cmd)
    time.sleep(0.1)
    TestSp.readline()
    print(Lum)
    Lum += 10'''