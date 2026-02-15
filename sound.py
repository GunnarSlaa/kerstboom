import sounddevice as sd
import numpy as np
from utilities import *
import math
import time as t
import queue
import getpass
import os

def effect_sound(coords, lights):
    neo = Pi5Neo('/dev/spidev0.0',LIGHTS_COUNT,800, quiet_mode=True)
    q = queue.Queue()

    def audio_callback(indata, outdata, frames, time, status):
        q.put(indata[::5, 0])

    def print_sound():
        try:
            data = q.get_nowait()
        except queue.Empty:
            return
        volume_norm = math.sqrt((np.linalg.norm(data))*12.0) * 4
        for light in range(lights):
            # if math.dist(coords[light], [0,0,0]) < volume_norm / 4:
            if coords[light][2] + 2 < volume_norm:
                neo.set_led_color(light, 15, 105, 0)
            else:
                neo.set_led_color(light, 0, 0, 20)
        neo.update_strip(sleep_duration=None)

    print(getpass.getuser())
    print(sd.query_devices())
    with sd.Stream(callback=audio_callback):
        t.sleep(0.5)
        while True:
            print_sound()

effect_sound(get_coords(), LIGHTS_COUNT)