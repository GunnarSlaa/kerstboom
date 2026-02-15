import statistics
import matplotlib.pyplot as plt

lights=350
minVal=100
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

x_list = []
y_list = []
z_list = []
    
for i in range(lights):
    zs = []
    xs = []
    ys = []
    if minY[i][0]>minVal:
        zs.append(minY[i][2])
        xs.append(minY[i][1])
    if minX[i][0]>minVal:
        zs.append(minX[i][2])
        ys.append(720 - minX[i][1])
    if plusY[i][0]>minVal:
        zs.append(plusY[i][2])
        xs.append(720 - plusY[i][1])
    if plusX[i][0]>minVal:
        zs.append(plusX[i][2])
        ys.append(plusX[i][1])
    if len(zs) == 0:
        print("Oh no!")
    if len(xs) == 0:
        print("no x!")
        xs.append(0)
    if len(ys) == 0:
        print("no y!")
        ys.append(0)
    z = statistics.mean(zs)
    x = statistics.mean(xs)
    y = statistics.mean(ys)
    x_list.append(x)
    y_list.append(y)
    z_list.append(z)
    with open("coords", "a") as f:
        f.write(f'{x} {y} {z}\n')

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')
ax.scatter(x_list, y_list, z_list)
ax.plot(x_list, y_list, z_list)
plt.show()
