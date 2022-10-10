#!/usr/bin/env python3

from lib.Utils import FilePaths, initialize_logger
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

class Settings(QWidget):
    '''
    This class initializes the window
    '''

    def __init__(self):
        super().__init__()
        self.logger = initialize_logger()
        self.file_paths = FilePaths()
        uic.loadUi(f'{self.file_paths.user_path}ui/Settings.ui',self)
