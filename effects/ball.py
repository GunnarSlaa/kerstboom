from utilities import *
import math
import sys

def setup(self, coords, colors):
    self.coords = rotate_x(20, coords)
    self.colors = colors
    self.size = 0
    self.speed = 0.007

def step(self, lights):
    frame = [self.colors[0]] * lights
    self.size += self.speed
    for light in range(lights):
        if math.dist(self.coords[light], [0,0,0]) < self.size:
            frame[light] = self.colors[1]
    if self.size >= 1.5:
        self.size = 0
        self.colors = self.colors[1:] + [self.colors[0]]
    return frame

kerstboom = Effect(setup, step, 0.01, 'bal', 'Bal effect!', ["BLUE", "ORANGE", "RED",  "GREEN","YELLOW"])
