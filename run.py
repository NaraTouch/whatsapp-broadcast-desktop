import sys
from PyQt5.QtWidgets import QApplication
from app.main import GUI

if __name__ == '__main__':
    app = QApplication([])
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())