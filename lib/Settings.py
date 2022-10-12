#!/usr/bin/env python3

from lib.Utils import FilePaths, initialize_logger
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

class Settings(QWidget):

    def __init__(self,main_window):
        super().__init__()
        self.logger = initialize_logger()
        self.file_paths = FilePaths()
        uic.loadUi(f'{self.file_paths.user_path}ui/Settings.ui',self)

        self.main_window = main_window

        self.log_fps_checkbox.stateChanged.connect(self.toggle_fps_log)
        self.debug_mode_checkbox.stateChanged.connect(self.toggle_debug_mode)
        self.reset_button.clicked.connect(self.reset_simulation)

    def toggle_debug_mode(self):
        if self.debug_mode_checkbox.isChecked():
            self.main_window.scene.set_debug_mode(True)
        else:
            self.main_window.scene.set_debug_mode(False)

    def toggle_fps_log(self):
        if self.log_fps_checkbox.isChecked():
            self.main_window.fps_log_timer.start(1000)
        else:
            self.main_window.fps_log_timer.stop()

    def reset_simulation(self):
        num_boids = self.boid_count_spinbox.value()
        self.main_window.scene.initialize_scene(num_boids=num_boids)
        self.toggle_debug_mode()
        self.toggle_fps_log()
