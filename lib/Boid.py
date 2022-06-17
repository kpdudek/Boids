#!/usr/bin/env python3

from lib.Utils import Logger,FilePaths
from lib.Physics2D import Physics2D
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import numpy as np
import json, time

class Boid(object):

    def __init__(self):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.config = None
        self.physics = Physics2D()
        self.theta_prev = 0.0
        self.load_config()

    def load_config(self):
        with open(f'{self.file_paths.entity_path}boid.json','r') as fp:
            self.config = json.load(fp)
        png_file = f"{self.file_paths.entity_path}{self.config['png_file']}"
        self.pixmap = QtGui.QPixmap(png_file).scaled(200, 200, Qt.KeepAspectRatio)
        self.draw_pixmap = QtGui.QPixmap(png_file).scaled(200, 200, Qt.KeepAspectRatio)

    def teleport(self,pose):
        self.physics.position = pose

    def update(self,force,time):
        self.physics.update(force,time)
        if self.physics.theta != self.theta_prev:
            self.draw_pixmap = self.pixmap.transformed(QtGui.QTransform().rotate(self.physics.theta))
        self.theta_prev = self.physics.theta
