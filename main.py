#!/usr/bin/env python3

import sys
from lib.Canvas import Canvas
from lib.Logger import Logger
from PyQt5.QtWidgets import QApplication
from lib.MainWindow import MainWindow

def main():
    logger = Logger()
    logger.insert_blank_lines(2)
    
    logger.log("Simulation starting...")
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    # canvas = Canvas(screen_resolution)
    main_window = MainWindow(screen_resolution)
    app.exec_()
    logger.log("Simulation ended.")

if __name__ == '__main__':
    main()