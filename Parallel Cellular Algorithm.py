import random

# Objective function
def f(x):
    return -x*x + 4*x + 1

# Parallel Cellular Algorithm
def parallel_cellular():
    random.seed(42)

    n = 10                  # Number of cells
    iterations = 50
    lower, upper = 0, 4

    # Initialize cells randomly
    cells = [random.uniform(lower, upper) for _ in range(n)]

    best = max(cells, key=f)

    for _ in range(iterations):

        old = cells.copy()   # Previous states (simultaneous update)
        new = []

        # Update each cell using its neighbors
        for i in range(n):

            # Left and right neighbors
            neighbors = old[max(0, i-1):min(n, i+2)]

            # Best neighbor
            nb = max(neighbors, key=f)

            # Move halfway towards the best neighbor
            x = old[i] + 0.5 * (nb - old[i])

            # Keep within bounds
            x = max(lower, min(upper, x))

            new.append(x)

        cells = new

        # Update best solution
        candidate = max(cells, key=f)

        if f(candidate) > f(best):
            best = candidate

    print("Best solution x:", round(best, 6))
    print("Maximum fitness:", round(f(best), 6))


parallel_cellular()
