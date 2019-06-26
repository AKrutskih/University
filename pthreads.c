#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <pthread.h>

#define n 3

    double x[n];
    double a[n][n] = {{1,2,3},{3,5,7},{1,3,4}};
    double b[n] = {3,0,1};

void pth_funk(void *arg)
{
    int k = * (int *) arg;
printf("%d", k);
double del_x = a[k][k];
    for (int i=k+1; i<n; i++)
    {
        double koef = a[i][k]/del_x;
        for (int j=k; j<n; j++)
            a[i][j] -= koef * a[k][j];
        b[i] -= koef * b[k];
    }
}

int main (int argc, char *argv[])
{

    //Печать
    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
        printf("%12.1f", a[i][j]);
        printf("%12.1f\n", b[i]);
    }

pthread_t tid[n];

    //Прямой
int arr[n-1];
for (int k=0; k<n-1; k++)
        {arr[k]=k;
pthread_create(&tid[k], NULL, pth_funk, (void *)&arr[k]);
}
for (int k=0; k<n-1; k++)
        pthread_join(tid[k], NULL);

    //Обратный
    for (int k = n-1; k>=0; k--)
    {
        x[k] = b[k];
        for (int i = k+1; i<n; i ++)
            x[k] -= a[k][i] * x[i];
        x[k] /= a[k][k];
    }

        //Печать х
        printf("\n");
        for (int j=0; j<n; j++)
            printf("%12.1f", x[j]);
        printf("\n");

return 0;
}
