#!/usr/bin/env python3

from lib.Utils import FilePaths, initialize_logger, set_logging_level
from PyQt5.QtWidgets import QWidget, QRadioButton
from PyQt5 import uic

class Settings(QWidget):

    def __init__(self,main_window,debug_mode):
        super().__init__()
        self.logger = initialize_logger()
        self.file_paths = FilePaths()
        uic.loadUi(f'{self.file_paths.user_path}ui/Settings.ui',self)

        self.main_window = main_window
        if debug_mode:
            self.debug_mode_checkbox.setChecked(True)
        
        self.log_fps_checkbox.stateChanged.connect(self.toggle_fps_log)
        self.debug_mode_checkbox.stateChanged.connect(self.toggle_debug_mode)
        self.reset_button.clicked.connect(self.reset_simulation)
        self.alignment_slider.valueChanged.connect(self.update_alignment)
        self.cohesion_slider.valueChanged.connect(self.update_cohesion)
        self.separation_slider.valueChanged.connect(self.update_separation)

        layout = self.tool_frame.layout()
        widgets = (layout.itemAt(i).widget() for i in range(layout.count()))
        for widget in widgets:
            if type(widget) == QRadioButton:
                widget.toggled.connect(self.update_tool_type)

    def update_tool_type(self,checked):
        if not checked:
            return
        if self.spawn_boid_radiobutton.isChecked():
            self.main_window.tool_type = "boid"
        elif self.spawn_obstacle_radiobutton.isChecked():
            self.main_window.tool_type = "obstacle"
        self.logger.info(f"Setting tool type to: {self.main_window.tool_type}")

    def update_cohesion(self):
        value = self.cohesion_slider.value() / 10.0
        self.main_window.scene.cohesion_multiplier = value
        self.cohesion_label.setText(f"Cohesion: {value}")

    def update_separation(self):
        value = self.separation_slider.value() / 10.0
        self.main_window.scene.separation_multiplier = value
        self.separation_label.setText(f"Separation: {value}")

    def update_alignment(self):
        value = self.alignment_slider.value() / 10.0
        self.main_window.scene.align_multiplier = value
        self.align_label.setText(f"Alignment: {value}")

    def toggle_debug_mode(self):
        if self.debug_mode_checkbox.isChecked():
            self.main_window.set_debug_mode(True)
            set_logging_level("DEBUG")
        else:
            self.main_window.set_debug_mode(False)
            set_logging_level("INFO")

    def toggle_fps_log(self):
        if self.log_fps_checkbox.isChecked():
            self.main_window.fps_log_timer.start(1000)
        else:
            self.main_window.fps_log_timer.stop()

    def reset_simulation(self):
        num_boids = self.boid_count_spinbox.value()
        max_vel = self.max_speed_spinbox.value()
        self.main_window.frame_idx = 0
        self.main_window.scene.initialize_scene(num_boids=num_boids,max_vel=max_vel)
        self.toggle_debug_mode()
        self.toggle_fps_log()
        self.update_alignment()
        self.update_cohesion()
        self.update_separation()
