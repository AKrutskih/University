import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

myMap = np.loadtxt('MAPS/Map25Iter0.txt')

fig = plt.figure ()
ax = plt.imshow (myMap , cmap = plt . get_cmap (" gist_earth ") )
fig.colorbar (ax)
fig.set_size_inches (8.5 , 8.5)
#fig.savefig ( file_name , dpi =100)
plt.close ( fig )
