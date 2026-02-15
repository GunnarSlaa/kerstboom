from utilities import *

def setup_plane(self, coords, colors):
    self.coords = coords
    self.colors = colors

def step_plane(self, lights):
    frame = [[[0,0,0],[0,0,0]]] * lights
    self.coords = rotate_y(-1, self.coords)
    for i in range(lights):
        if self.coords[i][2] < 0.1 and self.coords[i][2] > -0.1:
            frame[i] = self.colors[1]
        elif self.coords[i][2] > 0:
            frame[i] = self.colors[0]
        else:
            frame[i] = self.colors[2]
    return frame

plane = Effect(setup_plane, step_plane, 0.01, "plane", "Plane effect!", ["BLUE", "BLUE_ORANGE", "ORANGE"])
