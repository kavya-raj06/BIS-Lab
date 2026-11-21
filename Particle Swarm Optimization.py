%%writefile pso.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define NUM_DIMENSIONS 2

double func1(double position[]) {
    double total = 0.0;
    for (int i = 0; i < NUM_DIMENSIONS; i++) {
        total += position[i] * position[i];
    }
    return total;
}

double random_double(double min, double max) {
    return min + ((double)rand() / RAND_MAX) * (max - min);
}

typedef struct {
    double position[NUM_DIMENSIONS];
    double velocity[NUM_DIMENSIONS];
    double pos_best[NUM_DIMENSIONS];
    double err_best;
    double err;
} Particle;

void evaluate(Particle *particle,
              double (*costFunc)(double[])) {
    particle->err = costFunc(particle->position);
    if (particle->err < particle->err_best ||
        particle->err_best == -1) {

        for (int i = 0; i < NUM_DIMENSIONS; i++) {
            particle->pos_best[i] = particle->position[i];
        }
        particle->err_best = particle->err;
    }
}

void update_velocity(Particle *particle,
                     double pos_best_g[]) {
    double w = 0.5;
    double c1 = 1.0;
    double c2 = 2.0;
    for (int i = 0; i < NUM_DIMENSIONS; i++) {
        double r1 = random_double(0.0, 1.0);
        double r2 = random_double(0.0, 1.0);
        double vel_cognitive =
            c1 * r1 *
            (particle->pos_best[i] -
             particle->position[i]);
        double vel_social =
            c2 * r2 *
            (pos_best_g[i] -
             particle->position[i]);
        particle->velocity[i] =
            w * particle->velocity[i]
            + vel_cognitive
            + vel_social;
    }
}

void update_position(Particle *particle,
                     double bounds[][2]) {
    for (int i = 0; i < NUM_DIMENSIONS; i++) {
        particle->position[i] +=
            particle->velocity[i];
        if (particle->position[i] > bounds[i][1]) {
            particle->position[i] = bounds[i][1];
        }
        if (particle->position[i] < bounds[i][0]) {
            particle->position[i] = bounds[i][0];
        }
    }
}

void PSO(double (*costFunc)(double[]),
         double x0[],
         double bounds[][2],
         int num_particles,
         int maxiter) {
    double err_best_g = -1;
    double pos_best_g[NUM_DIMENSIONS];
    Particle swarm[num_particles];
    for (int i = 0; i < num_particles; i++) {
        for (int j = 0; j < NUM_DIMENSIONS; j++) {
            swarm[i].position[j] = x0[j];
            swarm[i].velocity[j] =
                random_double(-1.0, 1.0);
            swarm[i].pos_best[j] = x0[j];
        }
        swarm[i].err_best = -1;
        swarm[i].err = -1;
        evaluate(&swarm[i], costFunc);
    }
    int i = 0;
    while (i < maxiter) {
        for (int j = 0; j < num_particles; j++) {
           evaluate(&swarm[j], costFunc);
            if (swarm[j].err < err_best_g ||
                err_best_g == -1) {
                for (int k = 0; k < NUM_DIMENSIONS; k++) {
                    pos_best_g[k] =
                        swarm[j].position[k];
                }
                err_best_g = swarm[j].err;
            }
        }
        for (int j = 0; j < num_particles; j++) {
            update_velocity(&swarm[j], pos_best_g);
            update_position(&swarm[j], bounds);
        }
        i++;
    }
    printf("\nFINAL:\n");
    printf("Best Position: ");
    for (int i = 0; i < NUM_DIMENSIONS; i++) {
        printf("%lf ", pos_best_g[i]);
    }
    printf("\n");
    printf("Best Error: %lf\n", err_best_g);
}
int main() {
    srand((unsigned int)time(NULL));
    double initial[] = {5.0, 5.0};
    double bounds[NUM_DIMENSIONS][2] = {
        {-10.0, 10.0},
        {-10.0, 10.0}
    };
    int num_particles = 15;
    int maxiter = 30;
    PSO(func1,
        initial,
        bounds,
        num_particles,
        maxiter);
    return 0;
}

%%bash
gcc pso.c -o pso -lm
./pso
