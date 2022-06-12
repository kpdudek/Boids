#!/usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow, QCheckBox, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
from lib.Canvas import Canvas

from lib.Logger import FilePaths, Logger
from lib.Settings import Settings

class MainWindow(QMainWindow):
    '''
    This class initializes the window
    '''

    def __init__(self,screen_resolution):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        uic.loadUi(f'{self.file_paths.user_path}ui/MainWindow.ui',self)
        self.setWindowTitle('Boids')

        self.canvas = Canvas()
        self.canvas.shutdown_signal.connect(self.close)
        self.settings = Settings()
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.settings)
        self.show()

        window_size = [self.geometry().width(),self.geometry().height()]
        self.screen_width, self.screen_height = screen_resolution.width(), screen_resolution.height()
        offset_x = int((self.screen_width-window_size[0])/2)
        offset_y = int((self.screen_height-window_size[1])/2)
        self.setGeometry(offset_x,offset_y,window_size[0],window_size[1])

    def closeEvent(self, e):
        self.canvas.shutdown()
