lights=350

with open("coords") as f:
    coords = f.read().splitlines()
    coords = [[float(j) for j in i.split()] for i in coords]

for i in range(lights):
    for ax in range(3):
        if coords[i][ax] < 1:
            coords[i][ax] = (coords[i-1][ax] + coords[i+1][ax]) / 2
    with open("fixcoords", "a") as f:
        f.write(f'{coords[i][0]} {coords[i][1]} {coords[i][2]}\n')

