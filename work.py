import numpy as np
import random
import time
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from io import StringIO

'''
figure(num=None, figsize=(8, 6), dpi=100, facecolor='w', edgecolor='k')

x = np.arange(0, DIM)
y = np.arange(0, DIM)

X, Y = np.meshgrid(x, y)

ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, myMap, cmap='plasma', edgecolor='none')

plt.show()
'''

def generateStartAndEndPoints(myMap, numbersOfRobots):
    robotsPoints = np.empty((0, 2))
    endPoints = np.empty((0, 2))
    while (len(robotsPoints) != numbersOfRobots):
        flag = 0
        x = random.randint(0, len(myMap) - 1)
        y = random.randint(0, len(myMap) - 1)
        for i in range(len(robotsPoints)):
            if robotsPoints[i][0] == x and robotsPoints[i][1] == y:
                flag = 1
        if flag == 0:
            robotsPoints = np.append(robotsPoints, np.array([[x, y]]), axis=0)

    while (len(endPoints) != numbersOfRobots):
        flag = 0
        x = random.randint(0, len(myMap) - 1)
        y = random.randint(0, len(myMap) - 1)
        for i in range(len(robotsPoints)):
            if robotsPoints[i][0] == x and robotsPoints[i][1] == y:
                flag = 1
        for i in range(len(endPoints)):
            if endPoints[i][0] == x and endPoints[i][1] == y:
                flag = 1
        if flag == 0:
            endPoints = np.append(endPoints, np.array([[x, y]]), axis=0)
    return robotsPoints, endPoints


def LengthOfFly(myMap,StartPoints,EndPoints):
    matrix = np.empty((len(StartPoints),len(StartPoints)))
    for i in range(len(StartPoints)):
        for j in range(len(EndPoints)):
            matrix[i][j] = np.sqrt((StartPoints[i][0] - EndPoints[j][0])**2 + (StartPoints[i][1] - EndPoints[j][1])**2 + (myMap[StartPoints[i][0]][StartPoints[i][1]] - myMap[EndPoints[j][0]][EndPoints[j][1]])**2)
    return matrix

def chouseTarget (matrix):
    #print(len(matrix))
    endMatrix = np.zeros((0,2))
    efectMatrix = np.zeros((len(matrix),2))
    flag = np.zeros(len(efectMatrix))
    while len(endMatrix) < len(matrix):
        for i in range(len(matrix)):  # Выбор роботом самой выгодной цели
            chek = 1000000000
            if flag[i] != 2:
                for j in range(len(matrix)):
                    if matrix[i][j] < chek and matrix[i][j] != -1:
                        chek = matrix[i][j]
                        chekNomber = j
                efectMatrix[i][0] = chekNomber
                efectMatrix[i][1] = chek
        for i in range(len(efectMatrix)): #Закрепление одной цели за одним роботом
            if flag[i] != 2:
                flag[i] = 1
                for j in range(i):
                    if efectMatrix[i][0] == efectMatrix[j][0] and efectMatrix[i][1] <= efectMatrix[j][1] and flag[j] != 2:
                        flag [j] = 0
                    if efectMatrix[i][0] == efectMatrix[j][0] and efectMatrix[i][1] > efectMatrix[j][1] and flag[j] != 2:
                        flag [i] = 0
        #print (flag)
        #print('\n')
        for i in range(0,len(efectMatrix)):
            if flag[i] == 1:
                endMatrix = np.append(endMatrix, np.array([[i, efectMatrix[i][0]]]), axis = 0)
                for j in range(len(matrix)):
                    matrix[i][j] = -1
                    matrix[j][int(efectMatrix[i][0])] = -1
                flag[i] = 2
                #print (matrix)
                #print('\n')
    return endMatrix


def Astar(matrix, Xstart, Ystart, Xend, Yend):
    openPoints = np.empty((0,2), dtype=int)
    closePoints = np.empty((0, 2), dtype=int)
    pathFrom = np.empty((len(matrix), len(matrix), 2))
    openPoints = np.append(openPoints, np.array([[Xstart, Ystart]]), axis=0)
    weightG = np.zeros((len(matrix), len(matrix)))
    weightF = np.zeros((len(matrix), len(matrix)))
    weightG = weightG + 1000000000
    weightG[Xstart][Ystart] = 0
    weightF = weightF + 1000000000
    weightF[Xstart][Ystart] = 0
    while True:
        x, y = Fmin(openPoints, weightF)
        if x == Xend and y == Yend:
            return pathFrom
        openPoints = np.delete(openPoints, removeFromOpenedPoints(openPoints, x, y), axis=0)
        closePoints = np.append(closePoints, np.array([[x, y]]), axis=0)
        neighbours = searchNeighboursInClosedPoints(closePoints, x, y, len(matrix))
        for i in range(len(neighbours)):
            tempG = weightG[int(x), int(y)] + np.sqrt((matrix[int(x)][int(y)] - matrix[int(neighbours[i][0])][int(neighbours[i][1])])**2 + 1)
            if (searchNeighboursInOpen(openPoints, neighbours[i][0], neighbours[i][1]) == False) or (tempG < weightG[int(neighbours[i][0])][int(neighbours[i][1])]):  # IF (NEIGHBOUR NOT IN OPEN OR TEMP_G < G[NEIGHBOUR])
                pathFrom[int(neighbours[i][0])][int(neighbours[i][1])][0] = x
                pathFrom[int(neighbours[i][0])][int(neighbours[i][1])][1] = y  # FROM[NEIGHBOURS] = CURR (эта строка и та, что выше)
                weightG[int(neighbours[i][0])][int(neighbours[i][1])] = tempG  # G[NEIGHBOUR] = TEMP_G
                weightF[int(neighbours[i][0])][int(neighbours[i][1])] = weightG[int(neighbours[i][0])][int(neighbours[i][1])] + h(matrix,neighbours[i][0],neighbours[i][1],Xend,Yend)  # F[NEIGHBOUR] = G[NEIGHBOUR] + h(NEIGHBOUR, END)
            if searchNeighboursInOpen(openPoints, neighbours[i][0],neighbours[i][1]) == False:  # IF NEIGHBOUR NOT IN OPEN
                openPoints = np.append(openPoints, np.array([[neighbours[i][0], neighbours[i][1]]]),axis=0)  # ADD(NEIGHBOUR, OPEN)


def Fmin(openPoints, weightF):
    res = 1000000000
    x, y = 0, 0
    for i in range(len(openPoints)):
        if(weightF[int(openPoints[i][0])][int(openPoints[i][1])] < res):
            res = weightF[int(openPoints[i][0])][int(openPoints[i][1])]
            x = openPoints[i][0]
            y = openPoints[i][1]
    return x, y


def removeFromOpenedPoints(openPoints, x, y):
    for i in range(len(openPoints)):
        if (openPoints[i][0] == x) and (openPoints[i][1] == y):
            return i
    return -1


def searchNeighboursInClosedPoints(closedPoints, x, y, length):
    res = np.empty((0, 2))
    if (x - 1) >= 0:
        flag = 0
        for i in range(len(closedPoints)):
            if closedPoints[i][0] == x - 1 and closedPoints[i][1] == y:
                flag = 1
        if flag == 0:
            res = np.append(res, np.array([[x - 1, y]]), axis=0)

    if (x + 1) < length:
        flag = 0
        for i in range(len(closedPoints)):
            if closedPoints[i][0] == x + 1 and closedPoints[i][1] == y:
                flag = 1
        if flag == 0:
            res = np.append(res, np.array([[x + 1, y]]), axis=0)

    if (y - 1) >= 0:
        flag = 0
        for i in range(len(closedPoints)):
            if closedPoints[i][0] == x and closedPoints[i][1] == y - 1:
                flag = 1
        if flag == 0:
            res = np.append(res, np.array([[x, y - 1]]), axis=0)

    if (y + 1) < length:
        flag = 0
        for i in range(len(closedPoints)):
            if closedPoints[i][0] == x and closedPoints[i][1] == y + 1:
                flag = 1
        if flag == 0:
            res = np.append(res, np.array([[x, y + 1]]), axis=0)
    return res


def searchNeighboursInOpen(openPoints, x, y):
    for i in range(len(openPoints)):
        if openPoints[i][0] == x and openPoints[i][1] == y:
            return True
    return False


def h(matrix, Xstart, Ystart, Xend, Yend):
    return int(np.sqrt((Xend - Xstart) ** 2 + (Yend - Ystart) ** 2 + (matrix[int(Xstart)][int(Ystart)] - matrix[int(Xend)][int(Yend)]) ** 2))


def recoveryPath(pathMatrix, xStart, yStart, xEnd, yEnd):
    path = np.empty((0,2))
    x, y = xEnd, yEnd
    path = np.append(path, np.array([[x, y]]), axis=0)
    while (x != xStart) or (y != yStart):
        newX = pathMatrix[x][y][0]
        newY = pathMatrix[x][y][1]
        x, y = newX, newY
        #print(x, y, xStart, yStart)
        path = np.append(path, np.array([[x, y]]), axis=0)
    return path


#lenMap = [25, 50, 100, 250, 500, 1000]
#numbersOfRobots = [5, 10, 20, 50]

lenMap = [100]
numbersOfRobots = [5, 10, 20, 50]

for DIM in lenMap:
    for iterOfMap in range (10):
        myMap = np.loadtxt('MAPS/Map' + str(DIM) + 'Iter' + str(iterOfMap) + '.txt')
        for robot in numbersOfRobots:
            for iterOfRobots in range(10):

                startTime = time.time()
                st, en = generateStartAndEndPoints(myMap, robot)
                st = st.astype(int)
                en = en.astype(int)
                FlyPath = LengthOfFly(myMap, st, en)
                #FlyPath = FlyPath.astype(int)
                Targets = chouseTarget(FlyPath)
                Targets = Targets.astype(int)

                for i in range (robot):
                    #print(st[Targets[i][0]][0], st[Targets[i][0]][1], en[Targets[i][1]][0], en[Targets[i][1]][1])
                    #print('\n')
                    pathMatrix = Astar(myMap, st[Targets[i][0]][0], st[Targets[i][0]][1], en[Targets[i][1]][0], en[Targets[i][1]][1])
                    pathMatrix = pathMatrix.astype(int)
                    samePath = recoveryPath(pathMatrix, st[Targets[i][0]][0], st[Targets[i][0]][1], en[Targets[i][1]][0], en[Targets[i][1]][1])
                    samePath = samePath.astype(int)
                    #print(samePath)
                    #print('\n')

                file = open('TIME/Map' + str(DIM) + 'iter' + str(iterOfMap) + 'Rob' + str(robot) + 'iter' + str(iterOfRobots) + '.txt', 'w')
                file.write(str(time.time() - startTime) + '\n')
                file.close()
