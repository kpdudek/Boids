#!/usr/bin/env python3

from lib.Physics2D import Physics2D
from lib.Utils import Logger,FilePaths
import numpy as np
import json, time

class Boid(object):

    def __init__(self):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.config = None
        self.physics = Physics2D()
        self.load_config()

    def load_config(self):
        with open(f'{self.file_paths.user_path}entities/boid.json','r') as fp:
            self.config = json.load(fp)

    def teleport(self,pose):
        self.physics.position = pose

    def update(self,force,time):
        self.physics.update(force,time)
