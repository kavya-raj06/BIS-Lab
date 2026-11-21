import random

# Objective function
def f(x):
    return -x*x + 4*x + 1

# Convert binary chromosome to decimal and map to range [0, 4]
def decode(chromosome):
    decimal = int("".join(map(str, chromosome)), 2)
    return (decimal / 31) * 4

# Fitness function
def fitness(chromosome):
    x = decode(chromosome)
    return f(x)

# Generate initial population
def create_population(size):
    return [[random.randint(0, 1) for _ in range(5)]
            for _ in range(size)]

# Roulette wheel selection
def selection(population):
    return random.choices(
        population,
        weights=[fitness(c) for c in population],
        k=1
    )[0][:]

# Single point crossover
def crossover(p1, p2):
    point = random.randint(1, 4)
    c1 = p1[:point] + p2[point:]
    c2 = p2[:point] + p1[point:]
    return c1, c2

# Bit flip mutation
def mutation(chromosome, rate):
    for i in range(len(chromosome)):
        if random.random() < rate:
            chromosome[i] = 1 - chromosome[i]
    return chromosome

# Genetic Algorithm
def genetic_algorithm():
    random.seed(42)

    population_size = 10
    crossover_rate = 0.8
    mutation_rate = 0.1
    generations = 50

    population = create_population(population_size)
    best = None

    for gen in range(generations):

        # Evaluate and sort population
        population.sort(key=fitness, reverse=True)

        # Track best solution
        if best is None or fitness(population[0]) > fitness(best):
            best = population[0][:]

        # Elitism: preserve best chromosome
        new_population = [population[0][:]]

        while len(new_population) < population_size:

            # Selection
            p1 = selection(population)
            p2 = selection(population)

            # Crossover
            if random.random() < crossover_rate:
                c1, c2 = crossover(p1, p2)
            else:
                c1, c2 = p1[:], p2[:]

            # Mutation
            c1 = mutation(c1, mutation_rate)
            c2 = mutation(c2, mutation_rate)

            new_population.append(c1)

            if len(new_population) < population_size:
                new_population.append(c2)

        population = new_population

    # Final best solution
    population.sort(key=fitness, reverse=True)

    if fitness(population[0]) > fitness(best):
        best = population[0][:]

    x = decode(best)

    print("Best chromosome:", best)
    print("Best x:", round(x, 4))
    print("Maximum fitness:", round(fitness(best), 4))


genetic_algorithm()
