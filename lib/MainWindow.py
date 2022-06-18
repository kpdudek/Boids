#!/usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow, QCheckBox, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
from lib.Camera import Camera
from lib.Scene import Scene
import time

from lib.Utils import FilePaths, Logger
from lib.Settings import Settings
import numpy as np

class MainWindow(QMainWindow):
    '''
    This class initializes the window
    '''
    def __init__(self,screen_resolution):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        uic.loadUi(f'{self.file_paths.user_path}ui/MainWindow.ui',self)
        self.setWindowTitle('Boids')
        
        self.boundary_size = [1500,800]
        self.screen_width, self.screen_height = screen_resolution.width(), screen_resolution.height()
        offset_x = int((self.screen_width-self.boundary_size[0])/2)
        offset_y = int((self.screen_height-self.boundary_size[1])/2)
        self.setGeometry(offset_x,offset_y,self.boundary_size[0],self.boundary_size[1])

        self.keys_pressed = []
        self.scene = Scene(self.boundary_size)
        self.camera = Camera()
        self.camera.setScene(self.scene)
        self.camera.keypress_signal.connect(self.keyPressEvent)
        self.camera.keyrelease_signal.connect(self.keyReleaseEvent)
        self.settings = Settings()
        self.settings_visible = True
        self.settings.expand_collapse_settings_button.clicked.connect(self.expand_collapse_settings)
        
        self.layout.addWidget(self.camera)
        self.layout.addWidget(self.settings)
        self.setFocusPolicy(Qt.StrongFocus)
        self.show()

        self.is_shutting_down = False
        self.keys_pressed = []
        self.fps = 65.0
        self.loop_fps = 65.0
        self.delta_t = 0.0
        self.paused = False
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start(1000/self.fps)

        self.fps_log_timer = QTimer()
        self.fps_log_timer.timeout.connect(self.fps_log)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_C:
            self.camera.resetTransform()
        elif key == Qt.Key_P:
            if self.paused:
                self.logger.log('Resuming...')
                self.paused = False
            else:
                self.logger.log('Pausing...')
                self.paused = True
        elif key == Qt.Key_Q:
            self.scene.boids[0].physics.theta += 10
            self.scene.boids[0].pixmap.setRotation(self.scene.boids[0].physics.theta)
        elif key == Qt.Key_R:
            self.scene.boids[0].physics.theta -= 10
            self.scene.boids[0].pixmap.setRotation(self.scene.boids[0].physics.theta)
        elif key == Qt.Key_W:
            self.camera.translate(0,10)
        elif key == Qt.Key_S:
            self.camera.translate(0,-10)
        elif key == Qt.Key_A:
            self.camera.translate(10,0)
        elif key == Qt.Key_D:
            self.camera.translate(-10,0)
        elif key == Qt.Key_Z:
            self.camera.scale(.8,.8)
        elif key == Qt.Key_X:
            self.camera.scale(1.2,1.2)
        elif not event.isAutoRepeat():
            self.keys_pressed.append(key)
    
    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat() and event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())        

    def expand_collapse_settings(self):
        if self.settings_visible:
            self.settings.settings_frame.hide()
            self.settings_visible = False
            self.settings.expand_collapse_settings_button.setIcon(QIcon(f'{self.file_paths.user_path}ui/icons/expand_right.png'))
        else:
            self.settings.settings_frame.show()
            self.settings_visible = True
            self.settings.expand_collapse_settings_button.setIcon(QIcon(f'{self.file_paths.user_path}ui/icons/expand_down.png'))

    def fps_log(self):
        self.logger.log(f'Max FPS: {self.loop_fps}')
        if self.loop_fps<self.fps:
            self.logger.log("FPS has dropped below the set value.",color='y')

    def process_keys(self):
        cam_speed = 3.0

    def game_loop(self):
        # TODO: Make delta_t the time between last loop and this loop
        if self.paused:
            return
        
        self.process_keys()

        tic = time.time()
        force = np.zeros(2)
        t = 1.0 / self.fps
        self.scene.update(force,t)        
        toc = time.time()

        # Calculate max FPS
        self.delta_t = toc-tic
        if self.delta_t > 0.0:
            split_fps = 1.0/(toc-tic)
            self.loop_fps = (self.loop_fps + split_fps)/2.0
