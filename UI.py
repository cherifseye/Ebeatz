from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, 
                            QComboBox, QPushButton, QLabel, QCheckBox, QDialog, QLineEdit, 
                            QRadioButton, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
import pyqtgraph as pg
import serial
from serialPort import SerialPort


class EbeatzController(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMainWidget()
        self.setCentralRightFrame()
        self.setCentralLeftFrame()
        
    
    def initUI(self):
        self.setWindowTitle("Ebeatz Controller")
        self.resize(783, 545)
        self.setStyleSheet(
            "background-color: #1c2125;"
        )
        self.EbeatzSerial = SerialPort()
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
        self.centralLeftFrame.setFixedWidth(200) # Fixing the width of the left frame whatever the size of the win
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
        self.openCommunication.setText("Ouvrir Port")
        self.openCommunication.setMinimumHeight(30)
        self.openCommunication.clicked.connect(self.establishCommunication)
        self.openCommunication.setStyleSheet(
            "QPushButton"
            "{"
            "background-color: gray;"
            "color: white;"
            "border-radius: 10px;"
            "}"
            "QPushButton::pressed"
            "{"
            "background-color:green;"
            "}"
        )
        self.portLayout.addWidget(self.openCommunication)
        
        self.closeCommunication = QPushButton(self.portFrame)
        self.closeCommunication.setText("Fermer le Port")
        self.closeCommunication.setMinimumHeight(30)
        self.closeCommunication.clicked.connect(self.endCommunication)
        self.portLayout.addWidget(self.closeCommunication)
        self.closeCommunication.setStyleSheet(
            "QPushButton"
            "{"
            "background-color:gray;"
            "color:white;"
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
        #print(self.EbeatzSerial.portIsOpen())

    def endCommunication(self):
        self.EbeatzSerial.__closePort__()
        print(self.EbeatzSerial.portIsOpen())


    def setCentralLeftFrame(self):

        frequencyFrame = QFrame(self.centralLeftFrame)
        frequencyFrame.setStyleSheet(
            "background-color: #1c2125;"
        )
        frequencyFrame.setFixedHeight(80)
        frequencyFrame.setContentsMargins(0, 0, 0, 0)
        frequencyLayout = QHBoxLayout(frequencyFrame)
        self.centralLeftLayout.addWidget(frequencyFrame)

        frequencyDiplayFrame = QFrame(frequencyFrame)
        frequencyDiplayFrame.setContentsMargins(0, 0, 0, 0)
        frequencyDiplayFrame.setFixedWidth(170)
        frequencyDiplayFrame.setMinimumHeight(60)
        frequencyLayout.addWidget(frequencyDiplayFrame)
        frequencyDisplayLayout= QVBoxLayout(frequencyDiplayFrame)

        frequencyTitle = QLabel(frequencyDiplayFrame)
        frequencyTitle.setText("Frequence")
        frequencyTitle.setStyleSheet(
            "color: white;"
        )
        frequencyDisplayLayout.addWidget(frequencyTitle)
        frequencyTitle.setAlignment(Qt.AlignCenter)

        self.frequenceValueText = QLabel(frequencyDiplayFrame)
        self.frequenceValueText.setStyleSheet(
            "color:white;"
        )
        self.frequenceValueText.setAlignment(Qt.AlignCenter)
        self.frequenceValueText.setText("90 Hz")
        frequencyDisplayLayout.addWidget(self.frequenceValueText)

        setFrequencyValue = QPushButton(frequencyFrame)
        frequencyLayout.addWidget(setFrequencyValue)
        setFrequencyValue.setIcon(QIcon("Icons/swipe-right.png"))
        setFrequencyValue.setFlat(True)
        setFrequencyValue.setStyleSheet(
            "background-color: #1c2125;"
        )
        setFrequencyValue.clicked.connect(self.frequencyDialogSets)

        modeHarmoniqueFrame = QFrame(self.centralLeftFrame)
        self.centralLeftLayout.addWidget(modeHarmoniqueFrame)
        modeHarmoniqueFrame.setStyleSheet(
            "background-color: #1c2125;"
        )
        modeHarmoniqueFrame.setContentsMargins(0, 0, 0, 0)
        modeHarmoniqueFrame.setFixedHeight(80)
        modeHarmoniqueLayout = QVBoxLayout(modeHarmoniqueFrame)
        modeTitle = QLabel(modeHarmoniqueFrame)
        modeTitle.setText("Mode Harmonique")
        modeTitle.setStyleSheet("color:white;")
        modeHarmoniqueLayout.addWidget(modeTitle)
        modeTitle.setAlignment(Qt.AlignCenter)

        second_Harmonique = QRadioButton(modeHarmoniqueFrame)
        modeHarmoniqueLayout.addWidget(second_Harmonique)
        second_Harmonique.setText("2eme Harmonique")
        second_Harmonique.setStyleSheet(
            "color:white;"
        )


        AutoAccordFrame = QFrame(self.centralLeftFrame)
        AutoAccordFrame.setContentsMargins(0, 0, 0, 0)
        AutoAccordFrame.setFixedHeight(80)
        self.centralLeftLayout.addWidget(AutoAccordFrame)
        AutoAccordFrame.setStyleSheet("background-color: #1c2125;")
        AutoAccordLayout = QVBoxLayout(AutoAccordFrame)

        autoAccordTitle = QLabel(AutoAccordFrame)
        autoAccordTitle.setStyleSheet("color:white;")
        autoAccordTitle.setText("Auto Accord")
        AutoAccordLayout.addWidget(autoAccordTitle)
        autoAccordTitle.setAlignment(Qt.AlignCenter)
        
        activateAutoAccordButton = QRadioButton("Auto Accord Active")
        AutoAccordLayout.addWidget(activateAutoAccordButton)
        activateAutoAccordButton.setStyleSheet(
            "color: white;"
        )

        spaceItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.centralLeftLayout.addItem(spaceItem)
    
    def frequencyDialogSets(self):
        frequencyDialog = QDialog(self)
        frequencyDialog.setWindowTitle("Set Frequency")
        frequencyDialog.setStyleSheet('background-color: black')
        #self.setGeometry(100, 100, 100, 100)

        vbox = QVBoxLayout(frequencyDialog)
        self.line_edit = QLineEdit(frequencyDialog)
        self.line_edit.setFixedHeight(60)
        self.line_edit.setStyleSheet(
            "background-color: black;"
            "color: white;"
            "border: none;"
            "font-weight: bold;"
            "font-size: 20px;"
        )
        vbox.addWidget(self.line_edit)
  
        grid_layout = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['0', '.', 'OK']
        ]
        font  = QFont()
        font.setBold(True)
        font.setPointSize(14)

        for row in grid_layout:
            hbox = QHBoxLayout()
            for item in row:
                button = QPushButton(item)
                button.setFixedSize(50, 50)
                button.setStyleSheet(
                    "QPushButton"
                    "{"
                    "border-radius: 25px;"
                    "background-color: gray;"
                    "color: white;"
                    "}"
                )
                if item == "OK":
                    button.setStyleSheet(
                        "QPushButton"
                        "{"
                        "background-color: orange;"
                        "border-radius: 25px;"
                        "color: white;"
                        "}"
                    )
                button.setFont(font)
                button.clicked.connect(self.button_clicked)
                hbox.addWidget(button)
            vbox.addLayout(hbox)

    
        frequencyDialog.exec_()

    def ModeDialogSets(self):
        modeDialog = QDialog(self)
        modeDialog.setWindowTitle("Set Mode")
        modeDialog.setStyleSheet("background-color: #1c2125;")

        self.radio1 = QRadioButton("Harmonique 1")
        self.radio1.setStyleSheet("color:white")
        self.radio2 = QRadioButton("Harmonique 2")
        self.radio2.setStyleSheet("color:white")

        
        # Create "Apply" button
        self.apply_button = QPushButton("Apply")
        self.apply_button.setStyleSheet("color:white")
        self.apply_button.setFlat(True)
        
        # Create layout and add widgets
        layout = QVBoxLayout(modeDialog)
        layout.addWidget(self.radio1)
        layout.addWidget(self.radio2)
        layout.addWidget(self.apply_button)
        
        modeDialog.exec_()
         
    
    def button_clicked(self):
        button = self.sender()
        if button.text() == 'OK':
            pass
        
        else:
            self.line_edit.setText(self.line_edit.text() + button.text())