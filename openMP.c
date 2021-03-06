//openMP

#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <omp.h>

#define n 3

    double x[n];
    double a[n][n];
    double b[n];

int main (int argc, char *argv[])
{

    for (int i=0; i<n; i++)
    {
        srand(time(NULL));
        for (int j=0; j<n; j++)
            a[i][j] = rand() % 100 + 1;
        b[i] = rand() % 100 + 1;
    }

    //Печать
    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
        printf("%12.1f", a[i][j]);
        printf("%12.1f\n", b[i]);
    }

    //Прямой

#pragma omp parallel //num_threads(2)
{
# pragma omp for
for (int k=0; k<n-1; k++)
{
    double del_x = a[k][k];
    for (int i=k+1; i<n; i++)
    {
        double koef = a[i][k]/del_x;
        for (int j=k; j<n; j++)
            a[i][j] -= koef * a[k][j];
        b[i] -= koef * b[k];
    }
}
}

    //Обратный
    for (int k = n-1; k>=0; k--)
    {
        x[k] = b[k];
        for (int i = k+1; i<n; i ++)
            x[k] -= a[k][i] * x[i];
        x[k] /= a[k][k];
    }

printf("\n");
        for (int j=0; j<n; j++)
            printf("%12.1f", x[j]);
        printf("\n");

return 0;
}
