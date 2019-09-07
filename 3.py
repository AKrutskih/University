import numpy as np
import random
import time
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from io import StringIO


DIM = 25
i = 0
myMap = np.loadtxt('MAPS/Map' + str(DIM) + 'Iter' + str(i) + '.txt')
numbersOfRobots = 10

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


'''
def pathSelection(matrix, numbersOfRobots):
    selection = np.empty((0,2), dtype=int)
    i = 0
    while(len(selection) != numbersOfRobots):
        #print(matrix)
        j, rowMaximum, columnMaximum, flag = 0, 0, 0, 0
        rowMaximum = np.max(matrix[i])
        while(matrix[i][j] != rowMaximum):
            j = j + 1
        columnMaximum = np.max(matrix[:, j])
        if rowMaximum >= columnMaximum and columnMaximum != 0:
            selection = np.append(selection, np.array([[i, j]]), axis=0)
            for k in range(len(matrix)):
                matrix[:, j] = 0
                matrix[i] = 0
            i = 0
            flag = 1
        if flag != 1:
            i = i + 1
    return selection '''

def LenOfFly(myMap,StartPoints,EndPoints):
    matrix = np.empty((len(StartPoints),len(StartPoints)))
    for i in range(len(StartPoints)):
        for j in range(len(EndPoints)):
            matrix[i][j] = np.sqrt((StartPoints[i][0] - EndPoints[j][0])**2 + (StartPoints[i][1] - EndPoints[j][1])**2 + (myMap[StartPoints[i][0]][StartPoints[i][1]] - myMap[EndPoints[j][0]][EndPoints[j][1]])**2)
    return matrix

def chouseTarget (matrix):
    print(len(matrix))
    endMatrix = np.zeros((0,2))
    efectMatrix = np.zeros(len(matrix))
    flag = np.zeros(len(efectMatrix))
    while len(endMatrix) < len(matrix):
        for i in range(len(matrix)):  # Сортировка целей по выгоде
            chek = 1000000000000
            if flag[i] != 2:
                for j in range(len(matrix)):
                    if matrix[i][j] < chek and matrix[i][j] != -1:
                        chek = matrix[i][j]
                        chekNomber = j
                efectMatrix[i] = chekNomber
        if flag[0] != 2:
            flag[0] = 1
        for i in range(1,len(efectMatrix)): #Закрепление целей на данной итерации
            miniFlag = 0
            if flag[i] != 2:
                for j in range(i):
                    if efectMatrix[i] == efectMatrix[j]:
                        miniFlag = 1
                if miniFlag == 0:
                    flag[i] = 1
        #print (flag + '\n')
        for i in range(0,len(efectMatrix)):
            if flag[i] == 1:
                endMatrix = np.append(endMatrix, np.array([[i, efectMatrix[i]]]), axis = 0)
                for j in range(len(matrix)):
                    matrix[i][j] = -1
                    matrix[j][int(efectMatrix[i])] = -1
                flag[i] = 2
                #print (matrix + '\n')
    return endMatrix


st, en = generateStartAndEndPoints(myMap,numbersOfRobots)
st = st.astype(int)
en = en.astype(int)
pri = LenOfFly(myMap,st,en)
pri = pri.astype(int)

ppp = chouseTarget(pri)
ppp = ppp.astype(int)
print (ppp)

def Astar(matrix, start, end):
    openPoint = np.empty((0,2))
    closePoint = np.empty((0, 2))
    pathinside = np.empty((len(matrix), len(matrix), 2))
    openPoint = np.append(openPoint, np.array(start[0], start[1]))
    while workPoint != end:
        workPoint = min(openPoint)
