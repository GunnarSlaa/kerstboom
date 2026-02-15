from utilities import *

def setup(self, coords, colors):
    self.coords = coords
    self.colors = colors

def step(self, lights):
    frame = [[[0,0,0],[0,0,0]]] * lights
    self.coords = rotate_z(-1, self.coords)
    for i in range(lights):
        if self.coords[i][0] < 0:
            if self.coords[i][1] < 0:
                frame[i] = self.colors[0]
            else:
                frame[i] = self.colors[1]
        else:
            if self.coords[i][1] > 0:
                frame[i] = self.colors[2]
            else:
                frame[i] = self.colors[3]
    return frame

plane = Effect(setup, step, 0.01, "kermis", "Kermis effect!", ["BLUE", "RED", "GREEN", "YELLOW"])
