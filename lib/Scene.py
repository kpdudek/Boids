#!/usr/bin/env python3

import numpy as np
from random import randint
from PyQt5 import QtCore, QtWidgets
from lib.Utils import Logger, FilePaths

class Scene(QtWidgets.QWidget):
    shutdown_signal = QtCore.pyqtSignal()

    def __init__(self,fps):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()

        self.boids = []

    def initialize_scene(self):        
        self.logger.log(f'Initializing scene...')

    def update(self,force,time):
        for boid in self.boids:
            boid.update(force,time)