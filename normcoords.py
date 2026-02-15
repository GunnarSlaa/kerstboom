lights=350

with open("fixcoords") as f:
    coords = f.read().splitlines()
    coords = [[float(j) for j in i.split()] for i in coords]

maxZ = max([coord[2] for coord in coords])
minZ = min([coord[2] for coord in coords])
midZ = (maxZ + minZ) / 2
print(minZ, maxZ, midZ)

for i in range(lights):
    for ax in range(3):
        if coords[i][ax] < 1:
            coords[i][ax] = (coords[i-1][ax] + coords[i+1][ax]) / 2
    coords[i][0] = (coords[i][0] - 360) / 360
    coords[i][1] = (coords[i][1] - 360) / 360
    coords[i][2] = - (coords[i][2] - midZ) / (midZ - minZ)
    with open("normcoords", "a") as f:
        f.write(f'{coords[i][0]} {coords[i][1]} {coords[i][2]}\n')

