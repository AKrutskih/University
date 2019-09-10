import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

myMap = np.loadtxt('MAPS/Map25Iter0.txt')

fig  = plt.figure()
plt.colorbar(plt.imshow(myMap, origin="lower", cmap=cm.jet))
plt.title('Simple imshow plot')
'''for j in myMap:
    for i in j:
        plt.scatter(i[0][0], i[1][0], marker='D', linewidths=0.01, color='k')  # финиш
        plt.scatter(i[0][-1], i[1][-1], marker='o', linewidths=0.01, color='k')  # старт
        plt.plot(i[0], i[1], c='k', linewidth=1.2)'''
