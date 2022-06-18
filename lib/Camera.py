#!/usr/bin/env python3

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QLabel, QApplication, QGraphicsView
from PyQt5 import QtGui

from lib.Utils import Logger
from lib.Scene import Scene

import numpy as np
import time

class Camera(QGraphicsView):
    keypress_signal = pyqtSignal(QtGui.QKeyEvent)
    keyrelease_signal = pyqtSignal(QtGui.QKeyEvent)

    def __init__(self):
        super().__init__()
        
        self.camera = None
        self.logger = Logger()

        self.setResizeAnchor(QGraphicsView.NoAnchor)
        self.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.horizontalScrollBar().disconnect()
        self.verticalScrollBar().disconnect()
       
    def mousePressEvent(self, e):
        self.button = e.button()
        pose = np.array([e.x(),e.y()])
        self.logger.log(f'Mouse press ({self.button}) at: [{pose[0]},{pose[1]}]')
        if self.button == 1: # Left click
            pass
        elif self.button == 2: # Right click
            pass
        elif self.button == 4: # Wheel click
            pass
    
    def mouseMoveEvent(self, e):
        pose = np.array([e.x(),e.y()])
        if self.button == 1: # Left click
            pass
        elif self.button == 2: # Right click
            pass
        elif self.button == 4: # Wheel click
            pass
    
    def mouseReleaseEvent(self, e):
        pose = np.array([e.x(),e.y()])
        if self.button == 1: # Left click
            pass
        elif self.button == 2: # Right click
            pass
        elif self.button == 4: # Wheel click
            pass
        self.button = None
    
    def keyPressEvent(self, event):
        self.keypress_signal.emit(event)

    def keyReleaseEvent(self, event):
        self.keyrelease_signal.emit(event)