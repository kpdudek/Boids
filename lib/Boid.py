#!/usr/bin/env python3

import json
import numpy as np
from PyQt5 import QtGui
from math import degrees
from random import randint
from lib.Physics2D import Physics2D
from lib.Utils import Logger,FilePaths
from PyQt5.QtWidgets import QGraphicsPixmapItem

class Boid(object):

    def __init__(self,boundary_size):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.config = None
        self.physics = Physics2D()
        self.load_config()

        self.boundary_size = boundary_size
        self.theta_prev = 0.0

        vel_limit = 50
        vel_x = randint(-vel_limit,vel_limit)
        vel_y = randint(-vel_limit,vel_limit)
        self.steering_force = np.array([vel_x,vel_y])

    def load_config(self):
        with open(f'{self.file_paths.entity_path}boid.json','r') as fp:
            self.config = json.load(fp)
        png_file = f"{self.file_paths.entity_path}{self.config['png_file']}"

        pixmap = QtGui.QPixmap(png_file) #.scaled(200, 200, Qt.KeepAspectRatio)
        self.pixmap = QGraphicsPixmapItem(pixmap)
        self.pixmap.setTransformOriginPoint(pixmap.size().width()/2,pixmap.size().height()/2)

    def teleport(self,pose):
        self.physics.position = pose
        self.pixmap.setPos(pose[0],pose[1])

    def update(self,force,time):
        resulting_force = self.steering_force + force
        self.physics.update(resulting_force,time)
        self.theta_prev = self.physics.theta
        
        if self.physics.position[0] > self.boundary_size[0]:
            self.physics.position[0] = 0.0
        elif self.physics.position[0] < 0.0:
            self.physics.position[0] = self.boundary_size[0].copy()
        elif self.physics.position[1] > self.boundary_size[1]:
            self.physics.position[1] = 0.0
        elif self.physics.position[1] < 0.0:
            self.physics.position[1] = self.boundary_size[1].copy()
        
        pose = self.physics.position.copy()
        self.pixmap.setRotation(degrees(-self.physics.theta))
        self.pixmap.setPos(pose[0],pose[1])
