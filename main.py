"""
@author Kristen Kamouh
@date 18/2/2025
@description This file contains the main entry point for the application


"""

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())