import numpy as np
from mpi4py import MPI

def streams(total, SIZE, RANK):
    n = total
    q = n // SIZE
    r = SIZE * q - n

    chunk = q
    if (RANK >= SIZE - r):
        chunk = q - 1
    return chunk

SIZE = MPI.COMM_WORLD.Get_size()
RANK = MPI.COMM_WORLD.Get_rank()
NAME = MPI.Get_processor_name()

n = 100
t = MPI.Wtime()
nrows = streams(n, SIZE, RANK)
#a = [None]*nrows*(n+1)
#x = [None]*n
#tmp = [None]*(n+1)
tmp = np.ones(n+1)
a = np.ones(nrows*(n+1))
x = np.ones(n)
#x = np.arange (0, n, 1)
#x = range (0, n)
rows = np.ones(nrows+1)
#rows = [None]*nrows
for i in range(0, nrows):
    rows[i] = RANK + SIZE * i
    for j in range(0, n-1):
        a[i*(n-1)+j] = np.random.randint(1, 99)
    a[i*(n+1)+n] = np.random.randint(1, 99)

#if RANK == 0: print(rows)

row = 0
for i in range(0, n-1):
    if i == rows[row]:
        MPI.COMM_WORLD.Bcast (a[row * (n+1)], root = RANK)
        for j in range(0, n+1):
            tmp[j]=a[row*(n+1)+j]
        row = row + 1
    else:
        MPI.COMM_WORLD.Bcast (tmp, root = i // SIZE)
    for j in range(row, nrows):
        scaling = a[j*(n+1) + i] / tmp[i]
        for k in range(i, n+1):
            a[j * (n + 1) + k] = a[j*(n+1)+k] - scaling * tmp[k]

row = 0
for i in range(0, n):
    x[i] = 0
    if (i == rows[row]):
        x[i] = a[row*(n+1) + n]
        row = row + 1

row = nrows - 1
i = n-1
while i > 0:
    if (row >= 0):
        if (i == rows[row]):
            x[i] = x[i] / a[row * (n+1) + i]
            MPI.COMM_WORLD.Bcast (x[i], root = RANK)
            row = row - 1
        else:
            MPI.COMM_WORLD.Bcast (x[i], root = i // SIZE)
    else:
        MPI.COMM_WORLD.Bcast(x[i], root = i // SIZE)
    for j in range(0, row+1):
        x[rows[j]] = x[rows[j]] - a[j * (n+1) + i] * x[i]
    i = i - 1

if (RANK == 0):
    x[0] = x[0] / a[row * (n+1)]
MPI.COMM_WORLD.Bcast (x, root=0)

t = MPI.Wtime - t
if (RANK == 0):
    print("Time: ", t)

