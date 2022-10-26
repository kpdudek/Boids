#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from lib.Utils import initialize_logger
from lib.MainWindow import MainWindow
import sys

def main():
    debug_mode = False

    if "-d" in sys.argv:
        logger = initialize_logger(level="DEBUG")
        debug_mode = True
    else:
        logger = initialize_logger(level="INFO")
    
    logger.info(f"Simulation starting with options: {sys.argv[1:]}")
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    main_window = MainWindow(screen_resolution,debug_mode)
    app.exec_()
    logger.info("Simulation ended.")

if __name__ == '__main__':
    main()
