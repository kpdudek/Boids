#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from lib.Utils import initialize_logger
from lib.MainWindow import MainWindow
import sys

def main():
    logger = initialize_logger()
    logger.info("Simulation starting...")
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    main_window = MainWindow(screen_resolution)
    app.exec_()
    logger.info("Simulation ended.")

if __name__ == '__main__':
    main()
