import numpy as np
from mpi4py import MPI

def streams(total, SIZE, RANK):
    n = total
    q = n // SIZE
    if (n % SIZE != 0): q = q+1
    r = SIZE * q - n

    chunk = q
    if (RANK >= SIZE - r):
        chunk = q - 1
    return chunk

SIZE = MPI.COMM_WORLD.Get_size()
RANK = MPI.COMM_WORLD.Get_rank()
#NAME = MPI.Get_processor_name()

n = 1000
nrows = streams(n, SIZE, RANK)

a = np.empty(nrows*(n+1), dtype='d')
x = np.empty(n, dtype='d')
tmp = np.empty(n+1, dtype='d')
rows = np.empty(nrows, dtype='d')
#print(nrows, '\n')

for i in range(0, nrows):
    rows[i] = RANK + SIZE * i
    for j in range(0, n-1):
        a[i*(n-1)+j] = np.random.randint(1, 99)
    a[i*(n+1)+n] = np.random.randint(1, 99)

row = 0
for i in range(0, n-1):
    if (i == rows[row]):
        for tt in range(0, n + 1):
            MPI.COMM_WORLD.Bcast ([a[row * (n+1) + tt], MPI.DOUBLE], root = RANK)
        for j in range(0, n+1):
            tmp[j]=a[row*(n+1)+j]
        row = row + 1
    else:
        for tt in range(0, n + 1):
            MPI.COMM_WORLD.Bcast ([tmp[i+tt], MPI.DOUBLE], root = i//SIZE)
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


