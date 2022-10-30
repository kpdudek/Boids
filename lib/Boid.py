#!/usr/bin/env python3

from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsLineItem, QGraphicsEllipseItem
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from lib.Utils import initialize_logger, FilePaths
from lib.Physics2D import Physics2D
from PyQt5.QtCore import Qt
from random import randint
from math import degrees
from PyQt5 import QtGui
import numpy as np
import json

class Boid(object):

    def __init__(self,boundary_size,id,mass,max_vel,starting_pose):
        super().__init__()
        self.logger = initialize_logger()
        self.file_paths = FilePaths()
        self.id = id
        self.config = None
        self.load_config()
        self.physics = Physics2D(mass,max_vel,self.center_offset)
        self.teleport(starting_pose)
        self.logger.debug(f"Boid {id} spawned at position: {self.physics.position}")

        self.boundary_size = boundary_size
        self.theta_prev = 0.0

        vel_limit = 200
        vel_x = randint(-vel_limit,vel_limit)
        vel_y = randint(-vel_limit,vel_limit)
        self.steering_force = np.zeros(2)#np.array([vel_x,vel_y])

    def load_config(self):
        with open(f'{self.file_paths.entity_path}boid.json','r') as fp:
            self.config = json.load(fp)
        
        png_file = f"{self.file_paths.entity_path}{self.config['png_file']}"

        # Scale the pixmap based on the 1x2 array or keep default size if value is null
        pixmap = QtGui.QPixmap(png_file)
        x_size = pixmap.size().width()*self.config['png_scale'][0]
        y_size = pixmap.size().height()*self.config['png_scale'][1]
        if self.config['maintain_aspect']:
            pixmap = pixmap.scaled(x_size, y_size, Qt.KeepAspectRatio)
        else:
            pixmap = pixmap.scaled(x_size, y_size)
        mask = pixmap.createMaskFromColor(QtGui.QColor(0, 0, 0), Qt.MaskOutColor)
        p = QtGui.QPainter(pixmap)
        p.setPen(QtGui.QColor(randint(0,255), randint(0,255), randint(0,255)))
        p.drawPixmap(pixmap.rect(), mask, mask.rect())
        p.end()
        
        self.pixmap = QGraphicsPixmapItem(pixmap)
        x = pixmap.size().width()/2
        y = pixmap.size().height()/2
        self.center_offset = np.array([pixmap.size().width()/2,pixmap.size().height()/2])
        self.pixmap.setTransformOriginPoint(x,y)
        
        self.debug_line = QGraphicsLineItem(x+20,y,x+125,y,self.pixmap)

        rad = self.config['search_radius']
        self.debug_search_radius = QGraphicsEllipseItem(x-rad/2,y-rad/2,rad,rad,self.pixmap)

        self.debug_pose = QGraphicsRectItem(0,0,x_size,y_size,self.pixmap)
        self.debug_text = QGraphicsTextItem(str(self.id),self.pixmap)
        self.debug_text.setPos(0,-20)
        self.debug_text.setFont(QtGui.QFont("Arial",12))
    
    def set_debug_mode(self,enabled):
        if enabled:
            self.debug_line.show()
            self.debug_search_radius.show()
            self.debug_pose.show()
            self.debug_text.show()
        else:
            self.debug_line.hide()
            self.debug_search_radius.hide()
            self.debug_pose.hide()
            self.debug_text.hide()

    def teleport(self,pose):
        offset = pose.copy() - self.center_offset.copy()
        self.physics.position = offset.copy()
        self.physics.center_pose = self.physics.position + self.physics.center_offset
        self.pixmap.setPos(offset[0],offset[1])

    def rotate(self,angle):
        self.physics.theta = angle
        self.pixmap.setRotation(degrees(-angle))

    def update(self,force,time):
        resulting_force = self.steering_force + force
        
        self.physics.update(resulting_force,time)
        self.theta_prev = self.physics.theta

        # Wrap position within the boundary size
        if self.physics.center_pose[0] > self.boundary_size[0]:
            self.teleport(np.array([0.0,self.physics.position[1]]))
        elif self.physics.center_pose[0] < 0.0:
            self.teleport(np.array([self.boundary_size[0],self.physics.position[1]]))
        elif self.physics.center_pose[1] > self.boundary_size[1]:
            self.teleport(np.array([self.physics.position[0],0.0]))
        elif self.physics.center_pose[1] < 0.0:
            self.teleport(np.array([self.physics.position[0],self.boundary_size[1]]))
            
        pose = self.physics.position.copy()
        self.pixmap.setRotation(degrees(-self.physics.theta))
        self.pixmap.setPos(pose[0],pose[1])
