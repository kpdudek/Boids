#!/usr/bin/env python3

from lib.Utils import FilePaths, initialize_logger
from PyQt5.QtWidgets import QMainWindow
from lib.Physics2D import edge_angle
from PyQt5.QtCore import Qt, QTimer
from lib.Settings import Settings
from PyQt5.QtGui import QIcon
from lib.Camera import Camera
from lib.Scene import Scene
from lib.Boid import Boid
from typing import List
from PyQt5 import uic
import numpy as np
import time

class MainWindow(QMainWindow):

    def __init__(self,screen_resolution,debug_mode):
        super().__init__()
        self.logger = initialize_logger()
        self.file_paths = FilePaths()
        uic.loadUi(f'{self.file_paths.user_path}ui/MainWindow.ui',self)
        self.setWindowTitle('Boids')
        
        self.boundary_size = np.array([1800.0,800.0]) #[1500,800]
        window_size = np.array([1850.0,950.0])
        self.screen_width, self.screen_height = screen_resolution.width(), screen_resolution.height()
        offset_x = int((self.screen_width-window_size[0])/2)
        offset_y = int((self.screen_height-window_size[1])/2)
        self.setGeometry(offset_x,offset_y,window_size[0],window_size[1])
        
        self.selected_offset: np.ndarray = np.zeros(2)
        self.selected_boids: List[Boid] = []
        self.debug_mode = debug_mode
        self.keys_pressed = []
        self.loop_fps = 65.0
        self.paused = False
        self.delta_t = 0.0
        self.button = None
        self.fps = 65.0

        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.game_loop)

        self.fps_log_timer = QTimer()
        self.fps_log_timer.timeout.connect(self.fps_log)

        self.scene = Scene(self.boundary_size)

        self.camera = Camera()
        self.camera.setScene(self.scene)
        self.camera.keypress_signal.connect(self.keyPressEvent)
        self.camera.keyrelease_signal.connect(self.keyReleaseEvent)
        self.camera.mousepress_signal.connect(self.mousePressEvent)
        self.camera.mousemove_signal.connect(self.mouseMoveEvent)
        self.camera.mouserelease_signal.connect(self.mouseReleaseEvent)

        self.settings = Settings(self,debug_mode)
        self.settings_visible = True
        self.settings.expand_collapse_settings_button.clicked.connect(self.expand_collapse_settings)

        self.layout.addWidget(self.camera)
        self.layout.addWidget(self.settings)
        self.setFocusPolicy(Qt.StrongFocus)
        self.show()
        
        self.loop_count = 0
        self.frame_idx = 0
        self.settings.reset_simulation()
        self.game_timer.start(1000/self.fps)
    
    def mousePressEvent(self, e):
        self.button = e.button()
        pose = np.array([e.x(),e.y()])
        pose_scene = self.camera.mapToScene(pose[0],pose[1])
        pose_scene = np.array([pose_scene.x(),pose_scene.y()])
        self.logger.info(f'Mouse press ({self.button}) at screen: [{pose[0]},{pose[1]}], scene: [{int(pose_scene[0])},{int(pose_scene[1])}]')
        self.mouse_press = pose_scene.copy()

        if self.button == 1: # Left click
            for boid in self.scene.boids:
                if boid.pixmap.isUnderMouse():
                    self.selected_boids.append(boid)
                    self.selected_offset = boid.physics.center_pose - pose_scene
                    boid.teleport(pose_scene+self.selected_offset)
                    boid.physics.lock = True
            if len(self.selected_boids) > 0:
                return
            pose_scene = self.camera.mapToScene(pose[0],pose[1])
            pose_scene = np.array([pose_scene.x(),pose_scene.y()])
            max_vel = self.settings.max_speed_spinbox.value()
            self.scene.spawn_boid(max_vel,pose=pose_scene)
            self.scene.boids[-1].set_debug_mode(self.debug_mode)
            self.scene.boids[-1].physics.lock = True
        elif self.button == 2: # Right click
            for boid in self.scene.boids:
                if boid.pixmap.isUnderMouse():
                    self.scene.removeItem(boid.pixmap)
                    self.scene.boids.remove(boid)
                    self.scene.boid_count_display.setPlainText(f"Boids: {len(self.scene.boids)}")
        elif self.button == 4: # Wheel click
            pass

    def mouseMoveEvent(self, e):
        pose = np.array([e.x(),e.y()])
        pose_scene = self.camera.mapToScene(pose[0],pose[1])
        pose_scene = np.array([pose_scene.x(),pose_scene.y()])

        if self.button == 1: # Left click
            if len(self.selected_boids) > 0:
                for boid in self.selected_boids:
                    boid.teleport(pose_scene+self.selected_offset)
                return
            theta = edge_angle(np.zeros(2),pose_scene-self.mouse_press,np.array([100.0,0.0]))
            self.scene.boids[-1].rotate(theta)
        elif self.button == 2: # Right click
           pass
        elif self.button == 4: # Wheel click
            pass
    
    def mouseReleaseEvent(self, e):
        pose = np.array([e.x(),e.y()])
        pose_scene = self.camera.mapToScene(pose[0],pose[1])
        pose_scene = np.array([pose_scene.x(),pose_scene.y()])

        if self.button == 1: # Left click
            if len(self.selected_boids) > 0:
                for boid in self.selected_boids:
                    boid.teleport(pose_scene+self.selected_offset)
                    boid.physics.lock = False
                self.selected_boids = []
            velocity = pose_scene-self.mouse_press
            self.scene.boids[-1].physics.velocity = velocity
            self.scene.boids[-1].physics.lock = False
        elif self.button == 2: # Right click
            pass
        elif self.button == 4: # Wheel click
            pass
        self.button = None
    
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.shutdown()
        elif key == Qt.Key_C:
            self.camera.resetTransform()
        elif key == Qt.Key_P:
            if self.paused:
                self.logger.info('Resuming...')
                self.paused = False
            else:
                self.logger.info('Pausing...')
                self.paused = True
        elif key == Qt.Key_Space:
            if self.debug_mode:
                self.settings.debug_mode_checkbox.setChecked(False)
            else:
                self.settings.debug_mode_checkbox.setChecked(True)
        elif key == Qt.Key_N:
            self.frame_idx += 1
        elif not event.isAutoRepeat():
            self.keys_pressed.append(key)
    
    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat() and event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())

    def shutdown(self):
        self.logger.info('Shutdown called...')
        self.game_timer.stop()
        self.fps_log_timer.stop()
        self.close()
    
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
        self.logger.info(f'Max FPS: {self.loop_fps}')
        if self.loop_fps<self.fps:
            self.logger.warn("FPS has dropped below the set value.")

    def process_keys(self):
        cam_speed = 6.0
        zoom_speed = 0.008
        for key in self.keys_pressed:
            if key == Qt.Key_W:
                self.camera.translate(0,cam_speed)
            elif key == Qt.Key_S:
                self.camera.translate(0,-cam_speed)
            elif key == Qt.Key_A:
                self.camera.translate(cam_speed,0)
            elif key == Qt.Key_D:
                self.camera.translate(-cam_speed,0)
            elif key == Qt.Key_Z:
                self.camera.scale(1.0-zoom_speed,1.0-zoom_speed)
            elif key == Qt.Key_X:
                self.camera.scale(1.0+zoom_speed,1.0+zoom_speed)
    
    def set_debug_mode(self,enabled):
        self.scene.set_debug_mode(enabled)
        self.debug_mode = enabled
        self.frame_idx = self.loop_count

    def game_loop(self):
        # TODO: Make delta_t the time between last loop and this loop
        if self.paused:
            self.process_keys()
            return
        elif self.debug_mode and self.loop_count >= self.frame_idx:
            self.process_keys()
            return
        self.loop_count += 1
        self.logger.debug(f"Loop number: {self.loop_count}")            
        
        tic = time.time()
        self.process_keys()        
        t = 1.0 / self.fps
        self.scene.update(t)
        toc = time.time()

        # Calculate max FPS
        self.delta_t = toc-tic
        if self.delta_t > 0.0:
            split_fps = 1.0/(toc-tic)
            self.loop_fps = split_fps
            # self.loop_fps = (self.loop_fps + split_fps)/2.0
