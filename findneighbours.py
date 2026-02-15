import math
from pi5neo import Pi5Neo

lights=350
max_distance = 0.25
no_neighbours = 0

neo = Pi5Neo('/dev/spidev0.0',lights,800, quiet_mode=True)

with open("normcoords") as f:
    coords = f.read().splitlines()
    coords = [[float(j) for j in i.split()] for i in coords]

for i in range(lights):
    neighbours = []
    for j in range(lights):
        if i == j:
            continue
        if math.dist(coords[i], coords[j]) < max_distance:
            neighbours.append(j)
    # with open("neighbours", "a") as f:
    #     f.write(f'{i} {neighbours}\n')
    if len(neighbours) == 0:
        no_neighbours += 1
        neo.set_led_color(i, 255, 255, 255)

print(no_neighbours)
neo.update_strip(sleep_duration=0.02)
