from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QComboBox, QPushButton
import pyqtgraph as pg
import serial
import serialPort

class EbeatzController(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMainWidget()
        self.setCentralRightFrame()
        
    
    def initUI(self):
        self.setWindowTitle("Ebeatz Controller")
        self.resize(783, 545)
        self.setStyleSheet(
            "background-color: #1c2125;"
        )
        self.EbeatzSerial = serialPort.SerialPort()
    def setMainWidget(self):
        '''
        In these function we set a main widget and a central Horizontal layout in order to create the two main frame
        The first frame is the left frame that will contain some parameters such as changing the frequency or the mode
        The second frame align to the right occupe the most spaces and will contain the ports parameters and the graph
        To distinguish our two frame we're not using the same background color for them.
        '''
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralLayout = QHBoxLayout(self.centralWidget)

        self.centralLeftFrame = QFrame(self.centralWidget)
        self.centralLeftFrame.setFixedWidth(270) # Fixing the width of the left frame whatever the size of the win
        self.centralLeftFrame.setFrameShape(QFrame.StyledPanel)
        self.centralLeftFrame.setFrameShadow(QFrame.Raised)
        self.centralLeftFrame.setStyleSheet(
            "border-radius: 20px;"
            "background-color: #32373A;" #change the background color of the left frame
        )
        self.centralLeftLayout = QVBoxLayout(self.centralLeftFrame)
        self.centralLayout.addWidget(self.centralLeftFrame) #add the left frame to the central widget
      
        self.centralRightFrame = QFrame(self.centralWidget)
        self.centralRightLayout = QVBoxLayout(self.centralRightFrame)
        self.centralLayout.addWidget(self.centralRightFrame) # add the right frame to the central widget

    
    def setCentralRightFrame(self):
        '''
        In this code we set the contains of the right frame
        It will contain two main horizontal frame
        The first one will contains the settings of port communication
        The second one will contain the graph visualization of the frequencies
        '''

        self.portFrame = QFrame(self.centralRightFrame)
        self.portFrame.setFixedHeight(70)
        self.portLayout = QHBoxLayout(self.portFrame) #Create a horizontal layout for the port frame
        self.centralRightLayout.addWidget(self.portFrame)

        self.listPortAvalaible = QComboBox(self.portFrame)
        self.listPortAvalaible.setMinimumHeight(30)
        self.listPortAvalaible.setStyleSheet(
            "color: black;" #F2F3F4
            "background-color: gray;"
            "border-radius: 10px;"
        )
        self.listPortAvalaible.addItems(self.availablePort())
        self.portLayout.addWidget(self.listPortAvalaible)

        self.openCommunication = QPushButton(self.portFrame)
        self.openCommunication.setText("Open Port")
        self.openCommunication.setMinimumHeight(30)
        self.openCommunication.clicked.connect(self.establishCommunication)
        self.openCommunication.setStyleSheet(
            "QPushButton"
            "{"
            "background-color: gray;"
            "border-radius: 10px;"
            "}"
            "QPushButton::pressed"
            "{"
            "background-color:green;"
            "}"
        )
        self.portLayout.addWidget(self.openCommunication)
        
        self.closeCommunication = QPushButton(self.portFrame)
        self.closeCommunication.setText("Close")
        self.closeCommunication.setMinimumHeight(30)
        self.closeCommunication.clicked.connect(self.endCommunication)
        self.portLayout.addWidget(self.closeCommunication)
        self.closeCommunication.setStyleSheet(
            "QPushButton"
            "{"
            "background-color:gray;"
            "border-radius: 10px;"
            "}"
            "QPushButton::pressed"
            "{"
            "background-color:green;"
            "}"
        )
        
        self.plottingFrame = QFrame(self.centralRightFrame) #The frame will contain the plot space
        self.centralRightLayout.addWidget(self.plottingFrame)
        self.plottingLayout = QHBoxLayout(self.plottingFrame)
        self.graph = pg.PlotWidget(self.plottingFrame) #Creating the graph widget using pyqtgraph Module
        self.graph.setBackground("#1c2125")
        self.graph.setLabel("bottom", "time[s]")
        self.graph.setLabel("left", "Frequency [Hz]")
        self.graph.showGrid(True, True)
        self.graph.setAutoPan(True)
        self.plottingLayout.addWidget(self.graph)


    def availablePort(self) -> list[str]: #This function is used to return the list of available ports
        return self.EbeatzSerial.__getListPorts__()
    
    def establishCommunication(self):
        ser = serial.Serial(self.listPortAvalaible.currentText())
        self.EbeatzSerial.ser = ser
        print(self.EbeatzSerial.portIsOpen())

    def endCommunication(self):
        self.EbeatzSerial.__closePort__()
        print(self.EbeatzSerial.portIsOpen())