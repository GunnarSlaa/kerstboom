import math
import os
import signal
from pi5neo import Pi5Neo
import plotly.express as px

LIGHTS_COUNT = 350

COLORS={
    "GREEN" : [[100, 30, 0], [30, 120, 0]],
    "RED" : [[1, 100, 0], [220, 10, 0]],
    "YELLOW" : [[25, 105, 0], [255, 230, 0]],
    "BLUE" : [[0, 0, 255], [0, 0, 255]],
    "ORANGE" : [[25, 200, 0], [255, 125, 0]],
    "BLUE_ORANGE" : [[12,100,120], [200, 24, 200]],
}
    
def rotate_point_x(point, angle):
    newpoint = [0,0,0]
    newpoint[0] = point[0]
    newpoint[1] = math.cos(angle) * point[1] - math.sin(angle) * point[2]
    newpoint[2] = math.sin(angle) * point[1] + math.cos(angle) * point[2]
    return newpoint

def rotate_x(degrees, coords):
    new_coords = [rotate_point_x(point, degrees * (math.pi / 180)) for point in coords]
    return new_coords

def rotate_point_y(point, angle):
    newpoint = [0,0,0]
    newpoint[0] = math.cos(angle) * point[0] + math.sin(angle) * point[2]
    newpoint[1] = point[1]
    newpoint[2] = - math.sin(angle) * point[0] + math.cos(angle) * point[2]
    return newpoint

def rotate_y(degrees, coords):
    new_coords = [rotate_point_y(point, degrees * (math.pi / 180)) for point in coords]
    return new_coords

def rotate_point_z(point, angle):
    newpoint = [0,0,0]
    newpoint[0] = math.cos(angle) * point[0] - math.sin(angle) * point[1]
    newpoint[1] = math.sin(angle) * point[0] + math.cos(angle) * point[1]
    newpoint[2] = point[2]
    return newpoint

def rotate_z(degrees, coords):
    new_coords = [rotate_point_z(point, degrees * (math.pi / 180)) for point in coords]
    return new_coords

def claim_process():
    script_dir = os.path.dirname(__file__)
    pid = str(os.getpid())
    with open(os.path.join(script_dir, 'pid')) as f:
        running_pid = f.read()
        if running_pid != "":
            try:
                os.kill(int(running_pid), signal.SIGTERM)
            except ProcessLookupError:
                pass
    with open("pid", 'w') as f:
        f.write(pid)

def get_coords():
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, 'coords')) as f:
        coords = f.read().splitlines()
        coords = [[float(j) for j in i.split()] for i in coords]
    return coords

class Effect:
    instances = []

    def __init__(self, setup, step, sleep_duration, name, message, default_colors):
        self.setup = setup
        self.step = step
        self.sleep_duration = sleep_duration
        self.name = name
        self.message = message
        self.instances.append(self)
        self.default_colors = default_colors

    def run_effect(self, coords, lights, colors: list[list[list[int]]] = None):
        neo = Pi5Neo('/dev/spidev0.0',LIGHTS_COUNT,800, quiet_mode=True)
        if not colors:
            colors = [COLORS[i] for i in self.default_colors]
        self.setup(self, coords, colors)
        while True:
            frame = self.step(self, lights)
            for light in range(LIGHTS_COUNT):
                neo.set_led_color(light, *frame[light][0])
            neo.update_strip(sleep_duration=self.sleep_duration)

    def run_preview(self, coords, lights, colors: list[list[list[int]]] = None):
        steprate = int(0.2 / self.sleep_duration) if self.sleep_duration else 20
        output = coords * 50
        output = [[*i, 0, 0] for i in output]
        if not colors:
            colors = [COLORS[i] for i in self.default_colors]
        #Plotly needs all colors present in the first frame
        for color in colors:
            output.append([-10,-10,0,f'rgb({','.join(str(x) for x in color[1])})', 0])
        self.setup(self, coords, colors)
        for frame in range(50 * steprate):
            colors = self.step(self, lights)                
            if frame % steprate == 0:
                for light in range(LIGHTS_COUNT):
                    output[int(frame/steprate)*lights + light][3] = f'rgb({','.join(str(x) for x in colors[light][1])})'
                    output[int(frame/steprate)*lights + light][4] = int(frame/steprate)
        fig = px.scatter_3d(output, x=0, y=1, z=2, color=3, animation_frame=4, color_discrete_map='identity')
        fig.update_layout(
            scene = dict(
                xaxis = dict(range=[-1,1],),
                yaxis = dict(range=[-1,1],),))
        return fig

