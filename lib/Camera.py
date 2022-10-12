#!/usr/bin/env python3

from PyQt5.QtWidgets import QGraphicsView
from lib.Utils import initialize_logger
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui

class Camera(QGraphicsView):
    keypress_signal = pyqtSignal(QtGui.QKeyEvent)
    keyrelease_signal = pyqtSignal(QtGui.QKeyEvent)
    mousepress_signal = pyqtSignal(QtGui.QMouseEvent)
    mousemove_signal = pyqtSignal(QtGui.QMouseEvent)
    mouserelease_signal = pyqtSignal(QtGui.QMouseEvent)

    def __init__(self):
        super().__init__()        
        self.logger = initialize_logger()

        self.setResizeAnchor(QGraphicsView.NoAnchor)
        self.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.horizontalScrollBar().disconnect()
        self.verticalScrollBar().disconnect()
       
    def mousePressEvent(self, event):
        self.mousepress_signal.emit(event)
    
    def mouseMoveEvent(self, event):
        self.mousemove_signal.emit(event)
    
    def mouseReleaseEvent(self, event):
        self.mouserelease_signal.emit(event)
    
    def keyPressEvent(self, event):
        self.keypress_signal.emit(event)

    def keyReleaseEvent(self, event):
        self.keyrelease_signal.emit(event)

    def update(self):
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