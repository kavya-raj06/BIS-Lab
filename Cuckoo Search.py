import random
import math

# Objective function
def f(x):
    return -x*x + 4*x + 1

# Levy flight
def levy():
    beta = 1.5
    sigma = (
        math.gamma(1 + beta) * math.sin(math.pi * beta / 2) /
        (math.gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)
    ) ** (1 / beta)

    u = random.gauss(0, sigma)
    v = random.gauss(0, 1)

    return u / (abs(v)**(1 / beta))


# Cuckoo Search
def cuckoo_search():
    random.seed(42)

    n = 10                 # Number of nests
    pa = 0.25              # Discovery probability
    iterations = 100
    lower, upper = 0, 4

    # Initialize nests
    nests = [random.uniform(lower, upper) for _ in range(n)]

    best = max(nests, key=f)

    for _ in range(iterations):

        # Generate new solutions using Levy flight
        for i in range(n):
            step = levy()
            new = nests[i] + 0.01 * step * (nests[i] - best)

            # Keep solution within bounds
            new = max(lower, min(upper, new))

            # Greedy selection
            if f(new) > f(nests[i]):
                nests[i] = new

        # Abandon worst nests
        count = int(pa * n)
        worst = sorted(range(n), key=lambda i: f(nests[i]))[:count]

        for i in worst:
            nests[i] = random.uniform(lower, upper)

        # Update best solution
        candidate = max(nests, key=f)

        if f(candidate) > f(best):
            best = candidate

    print("Best solution x:", round(best, 6))
    print("Maximum fitness:", round(f(best), 6))


cuckoo_search()
