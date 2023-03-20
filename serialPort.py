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
             return [str(port).split(' ')[0] for port in ports.comports()]

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
        print(data)

'''
TestSp = SerialPort()
ser = serial.Serial('/dev/ttyACM0', baudrate=9600)
TestSp.ser = ser
while True:
    TestSp.sendCommand("High\n")
    time.sleep(2)
    TestSp.sendCommand("Low\n")
    time.sleep(2)
    TestSp.readline()
'''