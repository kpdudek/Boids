#!/usr/bin/env python3

import numpy as np
from PyQt5 import QtCore
from lib.Logger import Logger
from lib.PaintUtils import PaintUtils

class Camera(object):
    def __init__(self,window_size,painter,scene):
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.window_size = window_size
        self.painter = painter
        self.scene = scene
        self.zoom_level = 1.0

        self.frames = {
            'camera':np.array([0.0,0.0]),
            'scene':np.array([0.0,0.0])
            }

        self.display_fps_overlay = True

    def reset(self):
        self.teleport(np.zeros(2))

    def teleport(self,pose):
        self.frames['scene'] = pose
    
    def translate(self,vec):
        self.frames['scene'] = self.frames['scene'].copy() + -1*vec

    def zoom(self,multiplier):
        self.zoom_level = multiplier

    def transform(self,point,parent_frame='camera',child_frame='scene'):
        '''
        Transforms a point from the parent frame to the child frame.
        Default behavior is camera frame -> scene frame.
        '''
        coord = point + (self.frames[parent_frame] - self.frames[child_frame])
        return coord

    def clear_display(self):
        self.paint_utils.set_color(self.painter,'light_gray',True)
        self.painter.drawRect(0,0,self.window_size[0],self.window_size[1])

    def fps_overlay(self,fps):
        if self.display_fps_overlay:
            self.paint_utils.set_color(self.painter,'black',True)
            self.painter.drawText(3,13,200,75,QtCore.Qt.TextWordWrap,str(int(fps)))

    def paint_entity(self,boid):
        self.paint_utils.set_color(self.painter,'black',True,width=3)
        # pose = np.array([200.0,200.0])
        pose = boid.config['pose'].copy()
        pose_t = self.transform(pose)
        self.painter.drawEllipse(pose_t[0],pose_t[1],8,8)
        
    def update(self):
        '''
            Draws all entities in the scene.
        '''
        for boid in self.scene.boids:
            self.paint_entity(boid)
