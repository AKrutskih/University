#include <math.h>
#include <mpi.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
int streams(int total, int commsize, int rank)
{
    int n = total;
    int q = n / commsize;
    if (n % commsize != 0) q++;
    int r = commsize * q - n;

    int chunk = q;
    if (rank >= commsize - r) chunk = q - 1;
    return chunk;
}

int main(int argc, char *argv[])
{
    int n = 1000;
    int rank, commsize;
    MPI_Init(&argc,&argv);
    double t = MPI_Wtime();
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &commsize);

    int nrows = streams(n, commsize, rank);
    int *rows = malloc(sizeof(*rows) * nrows);
printf("%d, %d, %d\n", commsize, rank, nrows);
    double *a = malloc(sizeof(*a) * nrows * (n+1));
    double *x = malloc(sizeof(*x) * n);
    double *tmp = malloc(sizeof(*tmp) * (n+1));

    //Generate

    for (int i=0; i < nrows; i++)
    {
        rows[i] = rank + commsize * i;
        srand(time(NULL));
        for (int j=0; j<n; j++)
            a[i*(n+1)+j] = rand() % 100 + 1;
        //b
        a[i*(n+1)+n] = rand() % 100 + 1;
    }
    //Прямой
    int row = 0;
    for (int i=0; i<n-1; i++)
    {
        //Исключаем xi
        if (i == rows[row])
        {
            //Рассылка строки i
            MPI_Bcast(&a[row * (n+1)], n+1, MPI_DOUBLE, rank, MPI_COMM_WORLD);
            for (int j=0; j<=n; j++)
                tmp[j]=a[row * (n+1) + j];
            row++;
        }
        else
        {
            MPI_Bcast(tmp, n+1, MPI_DOUBLE, i % commsize, MPI_COMM_WORLD);
        }
        //Вычет строки
        for (int j=row; j<nrows; j++)
        {
            double scaling = a[j*(n+1) + i] / tmp[i];
            for (int k=i; k<n+1; k++)
                a[j*(n+1)+k] -= scaling * tmp[k];
        }
    }

    //"Грязная" инициализация x
    row = 0;
    for (int i=0; i<n; i++)
    {
        x[i]=0;
        if (i==rows[row])
        {
            x[i] = a[row*(n+1) + n];
            row++;
        }
    }

    //Обратный
    row = nrows-1;
    for (int i=n-1; i>0; i--)
    {
        if (row >= 0)
        {
            if (i == rows[row])
            {
                x[i] /= a[row * (n+1) +i];
                MPI_Bcast(&x[i], 1, MPI_DOUBLE, rank, MPI_COMM_WORLD);
                row--;
            }
            }
            else MPI_Bcast(&x[i], 1, MPI_DOUBLE, i%commsize, MPI_COMM_WORLD);
        }
        else MPI_Bcast(&x[i], 1, MPI_DOUBLE, i%commsize, MPI_COMM_WORLD);

        for (int j=0; j<=row; j++)
            x[rows[j]] -= a[j * (n+1) + i] * x[i];
    }

    if (rank == 0)
        x[0] /= a[row * (n+1)];
    MPI_Bcast(x, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    t = MPI_Wtime() - t;

    if (rank == 0)
        printf("Gauss MPI: n %d, procs %d, time (sec) %.6f\n", n, commsize, t);
        //printf("%d,%d,%d,%d,%d,%d \n", x[0], x[1], x[2], x[3], x[4], x[5]);
    MPI_Finalize();
    return 0;
}

