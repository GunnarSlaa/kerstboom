from utilities import *
from numpy import random
import math
import sys

def setup(self, coords, colors):
    self.offset = 0
    self.balls = [[random.normal(0, 0.5), random.normal(0, 0.5), random.uniform(1, 2), random.uniform(0.02, 0.03), random.uniform(0.1, 0.2)] for _ in range(7)]
    self.coords = coords
    self.colors = colors

def step(self, lights):
    frame = [[[0,0,0],[0,0,0]]] * lights
    for i, ball in enumerate(self.balls):
        ball[2] = ball[2] - ball[3]
        if ball[2] <= -1:
            self.balls[i] = [random.normal(0, 0.5), random.normal(0, 0.5), random.uniform(1, 2), random.uniform(0.02, 0.03), random.uniform(0.1, 0.2)]
        for light in range(lights):
            if math.dist(ball[:3], self.coords[light]) <= ball[4]:
                frame[light] = self.colors[0]
    return frame

balls = Effect(setup, step, 0.02, 'regen', 'Regen effect!', ["BLUE", "RED"])