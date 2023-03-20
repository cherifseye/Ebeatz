import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont, QColor
class Calculator(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setStyleSheet('background-color: black')
        #self.setGeometry(100, 100, 100, 100)

        vbox = QVBoxLayout()
        self.line_edit = QLineEdit()
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

        self.setLayout(vbox)

    
    def button_clicked(self):
        button = self.sender()
        if button.text() == 'OK':
            pass
        
        else:
            self.line_edit.setText(self.line_edit.text() + button.text())


if __name__ == "__main__":

    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys,exit(app.exec_())