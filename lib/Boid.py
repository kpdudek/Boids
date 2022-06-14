#!/usr/bin/env python3

from lib.Logger import Logger,FilePaths
import numpy as np
import json, time

class Boid(object):

    def __init__(self):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.config = None
        self.load_config()

    def load_config(self):
        with open(f'{self.file_paths.user_path}entities/boid.json','r') as fp:
            self.config = json.load(fp)
