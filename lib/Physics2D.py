#!/usr/bin/env python3

import numpy as np
from math import degrees
from lib.Geometry import edge_angle


class Physics2D(object):

    def __init__(self):
        super().__init__()

        self.time = None
        self.mass = 1.0
        self.theta = 0.0
        self.position = np.zeros(2)
        self.velocity = np.zeros(2)
        self.acceleration = np.zeros(2)

        self.max_velocity = 600.0

    def update(self,force,time):
        acceleration = force / self.mass
        delta_v = acceleration * time

        self.velocity = self.velocity + delta_v
        self.position = self.position + (self.velocity * time)
        self.theta = edge_angle(np.zeros(2),self.velocity.copy(),np.array([100.0,0.0]))

        # TODO: cap the magnitude, not each component individually
        if abs(self.velocity[0]) > self.max_velocity:
            self.velocity[0] = self.max_velocity * np.sign(self.velocity[0])
        if abs(self.velocity[1]) > self.max_velocity:
            self.velocity[1] = self.max_velocity * np.sign(self.velocity[1])
