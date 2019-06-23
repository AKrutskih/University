//openMP

#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <omp.h>

int main (int argc, char *argv[])
{
    int n = 1000;
//clock_t begin = clock();
    double *a = malloc(sizeof(*a) * n * n);
    double *b = malloc(sizeof(*b) * n);
    double *x = malloc(sizeof(*x) * n);

    for (int i=0; i<n; i++)
    {
        srand(time(NULL));
        for (int j=0; j<n; j++)
            a[i*n+j] = rand() % 100 + 1;
        b[i] = rand() % 100 + 1;
    }
    //Печать
    /*for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
            printf("%12.1f", a[i*n+j]);
        printf("%12.1f\n", b[i]);
    } */

        //omp_set_num_threads(10);

    //Прямой
    //#pragma opm parallel for
#pragma omp parallel //num_threads(5)
{
# pragma omp for
    for (int k=0; k<n-1; k++)
    {
        //Исключение Xi из всесх строк кроме К
        double del_x = a[k*n+k];
        for (int i = k+1; i<n; i++)
        {
            //Из строки i вычиаем строку k
            double koef = a[i*n+k]/del_x;
            for (int j=k; j<n; j++)
                a[i*n+j] -= koef * a[k*n+j];
            b[i] -= koef * b[k];
        }
    }
}

    //Обратный
    for (int k = n-1; k>=0; k--)
    {
        x[k] = b[k];
        for (int i = k+1; i<n; i ++)
            x[k] -= a[k*n+i] * x[i];
        x[k] /= a[k*n+k];
    }
    /*
    printf("\n");
    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
            printf("%12.1f", x[i*n+j]);
        printf("\n");
    } */
//clock_t end = clock();
//double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
//printf("\n %d \n", time_spent);
    return 0;
}
