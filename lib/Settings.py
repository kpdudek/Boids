#!/usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow, QCheckBox, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic

from lib.Utils import FilePaths, Logger

class Settings(QWidget):
    '''
    This class initializes the window
    '''

    def __init__(self):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        uic.loadUi(f'{self.file_paths.user_path}ui/Settings.ui',self)
