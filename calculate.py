import statistics
import plotly.express as px
from settings import *


with open("minY") as f:
    minY = f.read().splitlines()
    minY = [[int(line.split()[1].split('.')[0]), int(line.split('(')[1].split(',')[0]), int(line.split()[3].split(')')[0])] for line in minY]
with open("minX") as f:
    minX = f.read().splitlines()
    minX = [[int(line.split()[1].split('.')[0]), int(line.split('(')[1].split(',')[0]), int(line.split()[3].split(')')[0])] for line in minX]
with open("plusY") as f:
    plusY = f.read().splitlines()
    plusY = [[int(line.split()[1].split('.')[0]), int(line.split('(')[1].split(',')[0]), int(line.split()[3].split(')')[0])] for line in plusY]
with open("plusX") as f:
    plusX = f.read().splitlines()
    plusX = [[int(line.split()[1].split('.')[0]), int(line.split('(')[1].split(',')[0]), int(line.split()[3].split(')')[0])] for line in plusX]

coords = []
    
for i in range(LIGHTS_COUNT):
    xs, ys, zs = [], [], []
    if minY[i][0]>CALIBRATE_MIN_VAL:
        zs.append(minY[i][2])
        xs.append(minY[i][1])
    if minX[i][0]>CALIBRATE_MIN_VAL:
        zs.append(minX[i][2])
        ys.append(PICTURE_WIDTH - minX[i][1])
    if plusY[i][0]>CALIBRATE_MIN_VAL:
        zs.append(plusY[i][2])
        xs.append(PICTURE_WIDTH - plusY[i][1])
    if plusX[i][0]>CALIBRATE_MIN_VAL:
        zs.append(plusX[i][2])
        ys.append(plusX[i][1])
    if len(xs) == 0:
        xs.append(0)
    if len(ys) == 0:
        ys.append(0)
    if len(zs) == 0:
        zs.append(0)
    z = statistics.mean(zs)
    x = statistics.mean(xs)
    y = statistics.mean(ys)
    coords.append([x,y,z])

for i in range(LIGHTS_COUNT):
    for axis in range(3):
        if coords[i][axis] == 0:
            coords[i][axis] = (coords[i-1][axis] + coords[i+1][axis]) / 2

maxZ = max([coord[2] for coord in coords])
minZ = min([coord[2] for coord in coords])
midZ = (maxZ + minZ) / 2

for i in range(LIGHTS_COUNT):
    for axis in range(3):
        if coords[i][axis] < 1:
            coords[i][axis] = (coords[i-1][axis] + coords[i+1][axis]) / 2
    coords[i][0] = (coords[i][0]  / (PICTURE_WIDTH / 2)) - 1
    coords[i][1] = (coords[i][1]  / (PICTURE_WIDTH / 2)) - 1
    coords[i][2] = - (coords[i][2] - midZ) / (midZ - minZ)
    with open("coords", "a") as f:
        f.write(f'{coords[i][0]} {coords[i][1]} {coords[i][2]}\n')

fig = px.line_3d(coords, x=0, y=1, z=2, markers=True)
fig.update_layout(yaxis_range=[-1,1])
fig.show()