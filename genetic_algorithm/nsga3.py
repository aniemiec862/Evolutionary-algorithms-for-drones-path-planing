import math
import random

from genetic_algorithm.genetic_algorithm import OptimizationObjective
from uav.uav import UAV


class NSGA3:
    def run_generation(self, uavs: [UAV], selected_objectives: [OptimizationObjective], crossover_rate: float, mutation_rate: float):
        objectives = []
        for uav in uavs:
            objective_values = [0] * len(selected_objectives)
            for objective_id in range(len(selected_objectives)):
                objective_values[objective_id] = self.objective_function(uav, selected_objectives[objective_id])
            objectives.append(objective_values)

        print(objectives)

        # Non-dominated sorting
        fronts = self.non_dominated_sort(objectives)
        print(fronts)
        # Crowding distance calculation
        crowding_distances = []
        for f in fronts:
            crowding_distances += self.crowding_distance_assignment(f, objectives)

        new_population = []
        while len(new_population) < len(uavs):
            # Tournament selection
            parent1 = self.tournament_selection(uavs, crowding_distances)
            parent2 = self.tournament_selection(uavs, crowding_distances)

            # Crossover
            child = self.crossover(parent1, parent2, crossover_rate)

            # Mutation
            child = self.mutate(child, mutation_rate)

            new_population.append(child)

    @staticmethod
    def objective_function(uav: UAV, objective: OptimizationObjective):
        # Example: Assume a bi-objective optimization problem
        # where we aim to minimize two objectives: f1 and f2

        # Objective 1: Minimize f1
        if objective == OptimizationObjective.DISTANCE_FROM_OBJECTIVE:
            f1 = uav.calculate_distance_from_objective()
            return f1

        # Objective 2: Minimize f2
        elif objective == OptimizationObjective.TRAVELED_DISTANCE:
            f2 = uav.calculate_traveled_distance()
            return f2

        # Add more objectives as needed for multi-objective optimization

    def non_dominated_sort(self, objectives):
        population_size = len(objectives)
        dominance_matrix = [[0] * population_size for _ in range(population_size)]
        ranks = [0] * population_size
        fronts = []

        # Step 1: Dominance Matrix Calculation
        for i in range(population_size):
            for j in range(i + 1, population_size):
                if self.dominates(objectives[i], objectives[j]):
                    dominance_matrix[i][j] = 1
                elif self.dominates(objectives[j], objectives[i]):
                    dominance_matrix[j][i] = 1

        # Step 2: Rank Assignment
        # For each solution, it counts the number of solutions that dominate it. This count is stored in the ranks array.
        # If a solution has a rank of 0, it is considered part of the first front, and its index is added to the fronts list.
        for i in range(population_size):
            for j in range(population_size):
                if dominance_matrix[i][j] == 1:
                    ranks[i] += 1
            if ranks[i] == 0:
                fronts.append([i])
        # Step 3: Fronts Construction
        index = 0
        while len(fronts[index]) > 0:
            next_front = []

            for i in fronts[index]:
                for j in range(population_size):
                    if dominance_matrix[i][j] == 1:
                        ranks[j] -= 1

                        if ranks[j] == 0:
                            next_front.append(j)

            index += 1
            fronts.append(next_front)

        # The fronts list contains a list of fronts, where each front is represented by a list of indices corresponding
        # to solutions in that front. The fronts are ordered based on dominance relationships, with the first front
        # containing non-dominated solutions, and so on.
        return fronts

    # Crowding distance assignment
    @staticmethod
    def crowding_distance_assignment(front, objectives):
        population_size = len(front)
        distances = [0] * population_size
        for objective_index in range(len(objectives[0])):
            front = sorted(front, key=lambda x: objectives[x][objective_index])
            distances[objective_index] = math.inf
            distances[population_size - 1] = math.inf

            objective_min = objectives[front[0]][objective_index]
            objective_max = objectives[front[population_size - 1]][objective_index]

            if objective_max == objective_min:
                continue

            for i in range(1, population_size - 1):
                distances[i] += (objectives[front[i + 1]][objective_index] - objectives[front[i - 1]][
                    objective_index]) / (
                                        objective_max - objective_min)

        return distances

    @staticmethod
    def dominates(objective_values1, objective_values2):
        # Check if objective_values1 dominates objective_values2
        # Returns True if objective_values1 dominates objective_values2, False otherwise
        return all(o1 <= o2 for o1, o2 in zip(objective_values1, objective_values2))

    @staticmethod
    def tournament_selection(population, crowding_distances, tournament_size = 2):
        # # Randomly select individuals for the tournament
        # tournament_indices = random.sample(range(len(population)), tournament_size)
        #
        # # Create a list of tuples containing (index, crowding_distance)
        # candidates = [(index, crowding_distances[index]) for index in tournament_indices]
        #
        # # Select the individual with the highest crowding distance
        # winner_index = max(candidates, key=lambda x: x[1])[0]
        #
        # # Return the selected individual
        # return population[winner_index]
        pass

    @staticmethod
    def crossover(parent1, parent2, crossover_rate):
        # # Randomly determine whether to perform crossover
        # if random.random() > crossover_rate:
        #     # No crossover, return one of the parents
        #     return random.choice([parent1, parent2])
        #
        # # Randomly select a crossover point
        # crossover_point = random.randint(1, len(parent1))
        #
        # # Create a child by combining parts of both parents
        # child = parent1[:crossover_point] + parent2[crossover_point:]
        #
        # return child
        pass

    @staticmethod
    def mutate(individual, mutation_rate):
        # # Randomly determine whether to perform mutation
        # if random.random() > mutation_rate:
        #     # No mutation, return the original individual
        #     return individual
        #
        # # Randomly select a gene to mutate
        # mutated_gene_index = random.randint(0, len(individual) - 1)
        #
        # # Perform mutation (you may need a specific mutation operation based on your problem)
        # # For example, you could randomly change the value of the selected gene
        # individual[mutated_gene_index] = random_value_generation()
        #
        # return individual
        pass
