#!/usr/bin/env python
from utilities import *
import pkgutil
import importlib
import multiprocess as mp

coords = get_coords()
running_pid = None
script_dir = os.path.dirname(__file__)

effects = {}

for _, module_name, _ in pkgutil.iter_modules([os.path.join(script_dir, "effects")]):
    module = importlib.import_module(f"effects.{module_name}")
    for effect in Effect.instances:
        effects[effect.name] = effect

if __name__ != '__main__':
    mp.set_start_method('spawn')

def start_effect(effect: str, colors: list[str] = None):
    if colors:
        colors = [COLORS[i] for i in colors]
    global running_pid
    if running_pid:
        try:
            os.kill(int(running_pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
    if effect == "turnoff":
        return
    # p = mp.Process(target=effects[effect], args=(coords, LIGHTS_COUNT))
    p = mp.Process(target=effects[effect].run_effect, args=(coords, LIGHTS_COUNT, colors))
    p.start()
    running_pid = p.pid

if __name__ == '__main__':
    start_effect('kerstboom')