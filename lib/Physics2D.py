#!/usr/bin/env python3

from math import atan2
import numpy as np

def edge_angle(V0,V1,V2):
    '''
    The edge angle is found using unit vectors. This function is passed a set of three vertices where V0 is the shared point of the two vectors.
    Args:
        V0 (1x2 numpy array): Shared point of the two vectors
        V1 (1x2 numpy array): Vector 1 endpoint
        V2 (1x2 numpy array): Vector 2 endpoint
    '''
    # This function finds the signed shortest distance between two vectors
    V1[0] = V1[0] - V0[0]
    V1[1] = V1[1] - V0[1]
    V2[0] = V2[0] - V0[0]
    V2[1] = V2[1] - V0[1]

    # Dot product of the vectors
    cosine_theta = V1[0]*V2[0] + V1[1]*V2[1]
    # Cross product of the vectors
    sin_theta = V1[0]*V2[1] - V1[1]*V2[0]
    # find the angle using the relationships sin(theta)== tan(theta) = sin(theta)/cos(theta)
    edge_angle = atan2(sin_theta,cosine_theta)
    return edge_angle

class Physics2D(object):

    def __init__(self,mass,max_vel,center_offset):
        super().__init__()

        self.theta = 0.0
        self.mass = mass
        self.time = None
        self.lock : bool = False
        self.max_velocity = max_vel
        self.center_offset = center_offset
        self.position : np.ndarray = np.zeros(2)
        self.center_pose : np.ndarray = self.position + self.center_offset
        self.velocity : np.ndarray = np.zeros(2)
        self.acceleration : np.ndarray = np.zeros(2)

    def update(self,force,time):
        if self.lock:
            return
        acceleration = force / self.mass
        delta_v = acceleration * time

        self.velocity = self.velocity + delta_v
        self.position = self.position + (self.velocity * time)
        self.center_pose = self.position.copy() + self.center_offset.copy()
        if sum(self.velocity) > 0.001:
            self.theta = edge_angle(np.zeros(2),self.velocity.copy(),np.array([100.0,0.0]))
        
        # If the velocity exceeds the maximum magnitude, scale the velocity vector to match its value
        vel_mag = np.linalg.norm(self.velocity)
        if vel_mag > self.max_velocity:
            scale = self.max_velocity / vel_mag
            self.velocity = self.velocity * scale       
