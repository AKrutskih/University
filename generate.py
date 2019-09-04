import numpy as np
import random
import time
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from io import StringIO

def powerOfTwo(a):
    b = 1
    while (a > (2 ** b)):
        b = b + 1
    return 2**b

def fillTheMap(myMap, maxSize, size):
    x, y, half = size // 2, size // 2, size // 2
    if (half < 1):
        return myMap
    for y in range(half, maxSize, size):
        for x in range(half, maxSize, size):
            squareStep(myMap, x, y, half, int(random.uniform(-1, 1) * size * 0.2))

    for y in range(0, maxSize + 1, half):
        for x in range((y + half) % size, maxSize + 1, size):
            diamondStep(myMap, x, y, half, maxSize, int(random.uniform(-1, 1) * size * 0.2))

    fillTheMap(myMap, maxSize, size // 2)

def check(myMap, x, y, maxSize):
    if x < 0 or x > maxSize or y < 0 or y > maxSize:
        return -10000000
    else:
        return myMap[x][y]


def squareStep(myMap, x, y, size, offset):
    myMap[x][y] = (myMap[x+size][y+size] +  myMap[x-size][y+size] + myMap[x+size][y-size] + myMap[x-size][y-size]) // 4 + offset
    return myMap


def diamondStep(myMap, x, y, size, maxSize, offset):
    res = np.array([check(myMap, x, y+size, maxSize), check(myMap, x, y-size, maxSize),
           check(myMap, x+size, y, maxSize), check(myMap, x-size, y, maxSize)])
    value, length = 0, 0
    for i in range(len(res)):
        if res[i] != -10000000:
            value += res[i]
            length += 1
    myMap[x][y] = value // length + offset
    return myMap

KindOfSize = [25, 50, 100, 250, 500, 1000]

for DIM in KindOfSize:
    for i in range(10):
        size = powerOfTwo(DIM)
        myMap = np.zeros((size + 1, size + 1))

        myMap[0][0] = random.randint(100, 200)
        myMap[0][size] = random.randint(100, 200)
        myMap[size][0] = random.randint(100, 200)
        myMap[size][size] = random.randint(100, 200)

        fillTheMap(myMap, size, size)

        myMap = myMap[0:DIM, 0:DIM]
#myMap = myMap[(size - DIM) // 2 : (size - DIM) // 2 + DIM, (size - DIM) // 2 : (size - DIM) // 2 + DIM]
#print(myMap)

        '''figure(num=None, figsize=(8, 6), dpi=100, facecolor='w', edgecolor='k')

        x = np.arange(0, DIM)
        y = np.arange(0, DIM)

        X, Y = np.meshgrid(x, y)

        ax = plt.axes(projection='3d')
        ax.plot_surface(X, Y, myMap, cmap='plasma', edgecolor='none')

        #plt.show()'''

        np.savetxt('MAPS/Map' + str(DIM) + 'Iter' + str(i) + '.txt', myMap)


