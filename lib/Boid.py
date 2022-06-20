#!/usr/bin/env python3

import json
import numpy as np
from PyQt5 import QtGui
from math import degrees
from random import randint
from PyQt5.QtCore import Qt
from lib.Physics2D import Physics2D
from lib.Utils import Logger,FilePaths
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsLineItem

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

        # Scale the pixmap based on the 1x2 array or keep default size if value is null
        if self.config['png_scale']:
            x = self.config['png_scale'][0]
            y = self.config['png_scale'][1]
            pixmap = QtGui.QPixmap(png_file).scaled(x, y, Qt.KeepAspectRatio)
        else:
            pixmap = QtGui.QPixmap(png_file)
        
        self.pixmap = QGraphicsPixmapItem(pixmap)
        self.pixmap.setTransformOriginPoint(pixmap.size().width()/2,pixmap.size().height()/2)

        x = pixmap.size().width()/2
        y = pixmap.size().height()/2
        self.debug_line = QGraphicsLineItem(x+25,y,x+125,y,self.pixmap)
        self.debug_line.hide()

        starting_pose = np.array(self.config['pose'])
        self.teleport(starting_pose)

    def teleport(self,pose):
        self.physics.position = pose
        self.pixmap.setPos(pose[0],pose[1])

    def update(self,force,time):
        resulting_force = self.steering_force + force
        self.physics.update(resulting_force,time)
        self.theta_prev = self.physics.theta

        # Wrap position within the boundary size
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
