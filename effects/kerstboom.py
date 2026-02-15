from utilities import *
import copy

def setup(self, coords, colors):
    self.orig_coords = copy.deepcopy(coords)
    self.coords = rotate_x(20, coords)
    self.size = 0.3
    self.colors = colors[:-1]
    self.top_color = colors[-1]
    self.speed = 0.002
    self.lines = list(range(int(100 + self.size * 100), int(-100 - self.size * 100), int(-self.size * 100)))
    self.lines = [i / 100 for i in self.lines]

    self.offset = 0

def step(self, lights):
    frame = [[[0,0,0],[0,0,0]]] * lights
    self.offset += self.speed
    if self.offset >= self.size:
        self.offset = 0
        self.colors = self.colors[-1:] + self.colors[:-1]
    for i, line in enumerate(self.lines):
        for light in range(lights):
            if line - self.offset - self.size / 2 < self.coords[light][2] < line - self.offset + self.size / 2:
                frame[light] = self.colors[i % len(self.colors)]
    for light in range(lights):
        if self.orig_coords[light][2] > 0.7:
            frame[light] = self.top_color
    return frame

kerstboom = Effect(setup, step, 0.01, 'kerstboom', 'Kerstboom effect!', ["GREEN", "RED", "YELLOW"])
