import numpy as np

# Calculate distance between two locations
def distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))


# Ant Colony Optimization for Vehicle Routing
def vehicle_routing_aco(
    locations,
    n_ants,
    n_iterations,
    alpha,
    beta,
    evaporation_rate,
    Q
):

    n_locations = len(locations)

    # Initialize pheromone matrix
    pheromone = np.ones((n_locations, n_locations))

    best_route = None
    best_distance = float('inf')

    # Calculate distance matrix
    distances = np.zeros((n_locations, n_locations))

    for i in range(n_locations):
        for j in range(n_locations):
            distances[i][j] = distance(
                locations[i], locations[j]
            )

    distances[distances == 0] = 1e-10

    # Main optimization loop
    for iteration in range(n_iterations):

        routes = []
        route_lengths = []

        # Each ant constructs a delivery route
        for ant in range(n_ants):

            visited = [False] * n_locations

            # Start from depot (location 0)
            current_location = 0
            visited[0] = True

            route = [0]
            route_length = 0

            # Visit all customer locations
            while False in visited[1:]:

                unvisited = [
                    i for i in range(1, n_locations)
                    if not visited[i]
                ]

                probabilities = []

                # Calculate selection probabilities
                for next_location in unvisited:

                    probability = (
                        pheromone[current_location][next_location] ** alpha
                        *
                        (1 / distances[current_location][next_location]) ** beta
                    )

                    probabilities.append(probability)

                probabilities = np.array(probabilities)
                probabilities = probabilities / np.sum(probabilities)

                # Select next customer location
                next_location = np.random.choice(
                    unvisited,
                    p=probabilities
                )

                route.append(next_location)

                route_length += distances[
                    current_location
                ][next_location]

                visited[next_location] = True
                current_location = next_location

            # Return to depot
            route_length += distances[current_location][0]
            route.append(0)

            routes.append(route)
            route_lengths.append(route_length)

            # Update best route
            if route_length < best_distance:

                best_route = route.copy()
                best_distance = route_length

        # Pheromone evaporation
        pheromone *= (1 - evaporation_rate)

        # Pheromone updating
        for route, route_length in zip(routes, route_lengths):

            for i in range(len(route) - 1):

                start = route[i]
                end = route[i + 1]

                pheromone[start][end] += Q / route_length
                pheromone[end][start] += Q / route_length

        # print(
        #     f"Iteration {iteration + 1}: "
        #     f"Best Distance = {best_distance:.4f}"
        # )

    # Display final result
    print("\nBest Delivery Route:")

    for location in best_route:
        if location == 0:
            print("Depot", end=" -> ")
        else:
            print(f"Customer {location}", end=" -> ")

    print("\nTotal Travel Distance:", best_distance)


# Example usage

if __name__ == "__main__":

    # Location 0 represents the depot
    # Other locations represent customers

    locations = np.array([
        [0, 0],   # Depot
        [2, 3],   # Customer 1
        [5, 4],   # Customer 2
        [6, 1],   # Customer 3
        [3, 7],   # Customer 4
        [8, 6],   # Customer 5
        [1, 5],   # Customer 6
        [7, 3]    # Customer 7
    ])

    # Run vehicle routing optimization
    vehicle_routing_aco(
        locations,
        n_ants=10,
        n_iterations=100,
        alpha=1,
        beta=2,
        evaporation_rate=0.5,
        Q=1
    )
