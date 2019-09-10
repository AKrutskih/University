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


fig = plt . figure ()
59 ax = fig. add_subplot (111)
60 pl = ax. imshow ( graph . get_matrix () , cmap = plt . get_cmap (" gist_earth ") )
61 fig . colorbar (pl)
62 fig . set_size_inches (8.5 , 8.5)
63 ax. plot ([x for x, y in path ] , [y for x, y in path ] , linewidth =2.0 , c="
,→ orange ")
64 ax. plot ( path [0][0] , path [0][1] , "ro", c=" black ")
65 ax. plot ( path [len( path ) - 1][0] , path [ len ( path ) - 1][1] , "ro", c=" red ")
66 fig . savefig ( file_name , dpi =100)
67 plt . close ( fig )
