from PyQt5.QtCore import QThread,pyqtSignal

class Arduino(QThread):
    data_received = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.exiting = False
        self.list_data = []
    
    def __del__(self):
        self.exiting = True
        self.wait()
    
    def run(self):
        i = 0
        while not self.exiting:
            self.list_data.append(i)
            i += 1
           
            self.data_received.emit(self.list_data)
           
            if self.exiting:
               break
           
            QThread.msleep(400)