#!/usr/bin/env python3

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem
from lib.Utils import initialize_logger, FilePaths
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt
from random import randint
from lib.Boid import Boid
from PyQt5 import QtCore
import numpy as np

class Scene(QGraphicsScene):
    shutdown_signal = QtCore.pyqtSignal()

    def __init__(self,boundary_size):
        super().__init__()
        self.logger = initialize_logger()
        self.file_paths = FilePaths()

        self.boundary_size = boundary_size

    def initialize_scene(self,num_boids=50):        
        self.logger.info(f'Initializing scene with {num_boids} boids...')
        self.number_of_boids = num_boids

        # Remove all items
        self.boids = []
        items = self.items()
        for item in items:
            self.removeItem(item)

        self.setSceneRect(0,0,self.boundary_size[0],self.boundary_size[1])

        rect = QGraphicsRectItem(0.0,0.0,self.boundary_size[0],self.boundary_size[1])
        pen = QPen(Qt.black)
        pen.setWidth(3)
        rect.setPen(pen)
        self.addItem(rect)

        for i in range(self.number_of_boids):
            self.spawn_boid()

    def set_debug_mode(self,enabled):
        if enabled:
            for boid in self.boids:
                boid.set_debug_mode(True)
        else:
            for boid in self.boids:
                boid.set_debug_mode(False)

    def spawn_boid(self):
        rand_x = randint(0,self.boundary_size[0])
        rand_y = randint(0,self.boundary_size[1])
        boid = Boid(self.boundary_size)
        boid.teleport(np.array([rand_x,rand_y]))
        self.boids.append(boid)
        self.addItem(boid.pixmap)

    def update(self,force,time):
        for boid in self.boids:
            boid.update(force,time)