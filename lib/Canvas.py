#!/usr/bin/env python3

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5 import QtGui

from lib.Camera import Camera
from lib.Utils import Logger
from lib.Scene import Scene

import numpy as np
import time

class Canvas(QLabel):
    '''
    This class initializes the window
    '''
    shutdown_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        window_size = [800,400]

        self.is_shutting_down = False
        self.keys_pressed = []
        self.fps = 65.0
        self.loop_fps = 65.0
        self.delta_t = 0.0
        self.painter = None
        
        self.camera = None
        self.resize_canvas(window_size[0],window_size[1])
        self.logger = Logger()
        self.scene = Scene(self.fps)
        self.camera = Camera(self.painter,self.scene)

        self.paused = False
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start(1000/self.fps)

        self.fps_log_timer = QTimer()
        self.fps_log_timer.timeout.connect(self.fps_log)
        # self.fps_log_timer.start(1000)

        self.setFocusPolicy(Qt.StrongFocus)

    def resize_canvas(self,width,height):
        if isinstance(self.painter,QtGui.QPainter):
            if self.painter.isActive():
                self.painter.end()

        self.window_size = np.array([width,height])
        self.canvas_pixmap = QtGui.QPixmap(self.window_size[0],self.window_size[1])
        self.setPixmap(self.canvas_pixmap)
        self.painter = QtGui.QPainter(self.pixmap())

        if isinstance(self.camera,Camera):
            self.camera.painter = self.painter
            self.camera.window_size = self.window_size
            # self.camera.reset()

    def resizeEvent(self, e):
        self.resize_canvas(e.size().width(),e.size().height())

    def shutdown(self):
        if self.painter.isActive():
            self.painter.end()
        self.shutdown_signal.emit()

    def mousePressEvent(self, e):
        self.button = e.button()
        pose = np.array([e.x(),e.y()])
        self.logger.log(f'Mouse press ({self.button}) at: [{pose[0]},{pose[1]}]')

        if self.button == 1: # Left click
            pass
        elif self.button == 2: # Right click
            self.rmb_press_pose = pose
        elif self.button == 4: # Wheel click
            pass
    
    def mouseMoveEvent(self, e):
        pose = np.array([e.x(),e.y()])
        if self.button == 1: # Left click
            pass
        elif self.button == 2: # Right click
            self.camera.translate(pose-self.rmb_press_pose)
            self.rmb_press_pose = pose
        elif self.button == 4: # Wheel click
            # self.camera.translate(pose-self.wheel_press_pose)
            self.wheel_press_pose = pose
    
    def mouseReleaseEvent(self, e):
        button = e.button()
        pose = np.array([e.x(),e.y()])
        if button == 1: # Left click
            pass
        elif button == 2: # Right click
            self.rmb_press_pose = None
        elif button == 4: # Wheel click
            self.wheel_press_pose = None
    
    def keyPressEvent(self, event):
        key = event.key()
        if not event.isAutoRepeat():
            if key == Qt.Key_Escape:
                self.logger.log(f'Sending shutdown signal...')
                self.shutdown()
            elif key == Qt.Key_C:
                
                    self.camera.reset()
            elif key == Qt.Key_P:
                if self.paused:
                    self.logger.log('Resuming')
                    self.paused = False
                else:
                    self.paused = True
            elif key == Qt.Key_T:
                self.scene.boids[0].physics.theta += 10.0
            elif key == Qt.Key_R:
                self.scene.boids[0].physics.theta -= 10.0
            else:
                if key not in self.keys_pressed:
                    self.keys_pressed.append(key)

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat() and event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())

    def process_keys(self):
        cam_speed = 3.0
        for key in self.keys_pressed:
            if key == Qt.Key_A:
                self.camera.translate(np.array([cam_speed,0.0]))
            elif key == Qt.Key_D:
                self.camera.translate(np.array([-cam_speed,0.0]))
            elif key == Qt.Key_W:
                self.camera.translate(np.array([0.0,cam_speed]))
            elif key == Qt.Key_S:
                self.camera.translate(np.array([0.0,-cam_speed]))

    def fps_log(self):
        self.logger.log(f'Max FPS: {self.loop_fps}')
        if self.loop_fps<self.fps:
            self.logger.log("FPS has dropped below the set value.",color='y')

    def game_loop(self):
        # TODO: Make delta_t the time between last loop and this loop
        if self.paused:
            return
        
        self.process_keys()
        tic = time.time()
        force = np.zeros(2)
        # force[0] += 9.8
        t = 1.0 / self.fps
        self.scene.update(force,t)
        
        self.camera.clear_display()
        self.camera.update()
        self.camera.fps_overlay(self.loop_fps)
        
        self.repaint()
        toc = time.time()

        # Calculate max FPS
        self.delta_t = toc-tic
        if self.delta_t > 0.0:
            split_fps = 1.0/(toc-tic)
            self.loop_fps = (self.loop_fps + split_fps)/2.0
