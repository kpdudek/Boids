#!/usr/bin/env python3

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from lib.Utils import initialize_logger, FilePaths
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt
from random import randint
from lib.Boid import Boid
from PyQt5 import QtCore
from typing import List
import numpy as np

class Scene(QGraphicsScene):
    shutdown_signal = QtCore.pyqtSignal()

    def __init__(self,boundary_size):
        super().__init__()
        self.logger = initialize_logger()
        self.file_paths = FilePaths()

        self.id = 0
        self.boundary_size = boundary_size

        self.separation_multiplier = 0.0
        self.cohesion_multiplier = 0.0
        self.align_multiplier = 0.0
        self.x_offset = 0
        self.y_offset = 0

    def initialize_scene(self,num_boids=50,max_vel=400.0):        
        self.logger.info(f'Initializing scene with {num_boids} boids...')
        self.number_of_boids = num_boids
        self.id = 0

        # Remove all items
        self.boids: List[Boid] = []
        items = self.items()
        for item in items:
            self.removeItem(item)

        self.setSceneRect(0,0,self.boundary_size[0],self.boundary_size[1])

        rect = QGraphicsRectItem(0.0,0.0,self.boundary_size[0],self.boundary_size[1])
        pen = QPen(Qt.black)
        pen.setWidth(3)
        rect.setPen(pen)
        self.addItem(rect)
        
        self.boid_count_display = QGraphicsTextItem(f"Boids: {len(self.boids)}")
        self.addItem(self.boid_count_display)

        for i in range(self.number_of_boids):
            self.spawn_boid(max_vel)

    def set_debug_mode(self,enabled):
        if enabled:
            for boid in self.boids:
                boid.set_debug_mode(True)
        else:
            for boid in self.boids:
                boid.set_debug_mode(False)

    def spawn_boid(self,max_vel,pose=None):
        if not isinstance(pose,np.ndarray):
            rand_x = randint(0,self.boundary_size[0])
            rand_y = randint(0,self.boundary_size[1])
            pose = np.array([rand_x,rand_y])
        boid = Boid(self.boundary_size,self.id,1.0,max_vel,pose)
        self.id += 1
        self.boids.append(boid)
        self.addItem(boid.pixmap)
        self.boid_count_display.setPlainText(f"Boids: {len(self.boids)}")

    def update(self,time):
        # For each boid, find it's nearest neighbors
        # by checking if their position lies within a certain raius
        forces = []
        for idx,boid in enumerate(self.boids):
            neighbor_ids = []
            distances = []
            velocities = []
            positions = []
            offsets = []
            for neighbor_idx,other_boid in enumerate(self.boids):
                # Don't skip yourself. You're part of the group.
                distance = np.linalg.norm(boid.physics.center_pose-other_boid.physics.center_pose)
                if distance < boid.config['search_radius']:
                    # nearest_neighbors.append(other_boid)
                    neighbor_ids.append(neighbor_idx)
                    distances.append(distance)
                    velocities.append(other_boid.physics.velocity.copy())
                    positions.append(other_boid.physics.center_pose.copy())
                    offsets.append(other_boid.physics.position - boid.physics.position)
                
            num_nearest_neighbors = len(neighbor_ids)
            if num_nearest_neighbors > 1:
                separation_force = -1.0 * (sum(offsets)/num_nearest_neighbors) * self.separation_multiplier
                cohesion_force = (sum(positions)/num_nearest_neighbors) * self.cohesion_multiplier
                align_force = (sum(velocities)/num_nearest_neighbors) * self.align_multiplier
                force = align_force + separation_force + cohesion_force

                self.logger.debug(f"Boid {boid.id} has neighbors: {neighbor_ids}")
                self.logger.debug(f"\tPosition: {boid.physics.position}")
                self.logger.debug(f"\tSteering force: {boid.steering_force}")
                self.logger.debug(f"\tVelocity: {boid.physics.velocity}")
                self.logger.debug(f"\tAlign force: {force}")
            else:
                force = np.zeros(2)

            forces.append(force)

        for idx,boid in enumerate(self.boids):
            boid.update(forces[idx],time)