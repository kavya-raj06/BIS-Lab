%%writefile gwo.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define DIM 2
#define NUM_WOLVES 10
#define MAX_ITERATIONS 100

#define LOWER_BOUND 0.0
#define UPPER_BOUND 30.0

/* Generate a random number between 0 and 1 */
double random_double()
{
    return (double)rand() / RAND_MAX;
}

/* Objective function: Sphere function
   Minimum value is 0 at (0, 0) */
double fitness_function(double x[])
{
    double sum = 0.0;
    int i;

    for (i = 0; i < DIM; i++)
    {
        sum += x[i] * x[i];
    }

    return sum;
}

/* Keep wolf positions within the search space */
void bound_position(double x[])
{
    int i;

    for (i = 0; i < DIM; i++)
    {
        if (x[i] < LOWER_BOUND)
            x[i] = LOWER_BOUND;

        if (x[i] > UPPER_BOUND)
            x[i] = UPPER_BOUND;
    }
}

int main()
{
    double wolves[NUM_WOLVES][DIM];
    double alpha[DIM], beta[DIM], delta[DIM];
    double alpha_score, beta_score, delta_score;
    double a, r1, r2;
    double A1, A2, A3, C1, C2, C3;
    double D_alpha, D_beta, D_delta;
    double X1, X2, X3;
    double new_positions[NUM_WOLVES][DIM];
    double fitness;
    int i, j, iter;

    srand((unsigned int)time(NULL));

    /* Initialize alpha, beta, and delta scores */
    alpha_score = INFINITY;
    beta_score = INFINITY;
    delta_score = INFINITY;

    /* Initialize wolf population */
    for (i = 0; i < NUM_WOLVES; i++)
    {
        for (j = 0; j < DIM; j++)
        {
            wolves[i][j] =
                LOWER_BOUND +
                random_double() * (UPPER_BOUND - LOWER_BOUND);
        }
    }

    /* Main GWO loop */
    for (iter = 0; iter < MAX_ITERATIONS; iter++)
    {
        /* Evaluate fitness and identify leaders */
        for (i = 0; i < NUM_WOLVES; i++)
        {
            fitness = fitness_function(wolves[i]);

            if (fitness < alpha_score)
            {
                delta_score = beta_score;
                for (j = 0; j < DIM; j++)
                    delta[j] = beta[j];

                beta_score = alpha_score;
                for (j = 0; j < DIM; j++)
                    beta[j] = alpha[j];

                alpha_score = fitness;
                for (j = 0; j < DIM; j++)
                    alpha[j] = wolves[i][j];
            }
            else if (fitness < beta_score)
            {
                delta_score = beta_score;
                for (j = 0; j < DIM; j++)
                    delta[j] = beta[j];

                beta_score = fitness;
                for (j = 0; j < DIM; j++)
                    beta[j] = wolves[i][j];
            }
            else if (fitness < delta_score)
            {
                delta_score = fitness;
                for (j = 0; j < DIM; j++)
                    delta[j] = wolves[i][j];
            }
        }

        /* Parameter a decreases linearly from 2 to 0 */
        a = 2.0 - 2.0 * iter / MAX_ITERATIONS;

        /* Update positions of all wolves */
        for (i = 0; i < NUM_WOLVES; i++)
        {
            for (j = 0; j < DIM; j++)
            {
                r1 = random_double();
                r2 = random_double();
                A1 = 2.0 * a * r1 - a;
                C1 = 2.0 * r2;

                D_alpha = fabs(C1 * alpha[j] - wolves[i][j]);
                X1 = alpha[j] - A1 * D_alpha;

                r1 = random_double();
                r2 = random_double();
                A2 = 2.0 * a * r1 - a;
                C2 = 2.0 * r2;

                D_beta = fabs(C2 * beta[j] - wolves[i][j]);
                X2 = beta[j] - A2 * D_beta;

                r1 = random_double();
                r2 = random_double();
                A3 = 2.0 * a * r1 - a;
                C3 = 2.0 * r2;

                D_delta = fabs(C3 * delta[j] - wolves[i][j]);
                X3 = delta[j] - A3 * D_delta;

                new_positions[i][j] = (X1 + X2 + X3) / 3.0;
            }
        }

        /* Apply all position updates simultaneously */
        for (i = 0; i < NUM_WOLVES; i++)
        {
            for (j = 0; j < DIM; j++)
                wolves[i][j] = new_positions[i][j];

            bound_position(wolves[i]);
        }

        /* Display progress every 10 iterations */
        if ((iter + 1) % 10 == 0)
        {
            printf("Iteration %d: Best Fitness = %.8f\n",
                   iter + 1, alpha_score);
        }
    }

    /* Output the best solution */
    printf("\nOptimal Solution:\n");

    for (j = 0; j < DIM; j++)
    {
        printf("x%d = %.8f\n", j + 1, alpha[j]);
    }

    printf("Minimum Fitness = %.8f\n", alpha_score);

    return 0;
}

!gcc -O3 gwo.c -o gwo -lm
!./gwo
