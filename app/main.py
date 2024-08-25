import sys
from PyQt5.QtWidgets import QApplication
from app.gui import GUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())