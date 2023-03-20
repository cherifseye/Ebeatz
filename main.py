from PyQt5.QtWidgets import QApplication
import UI
import sys

def main():
    app = QApplication(sys.argv)
    win = UI.EbeatzController()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
