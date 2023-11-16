import math
import random

from genetic_algorithm.genetic_algorithm import OptimizationObjective
from uav.genotype import Genotype, MoveGene
from uav.uav import UAV


class CrowdingDistanceResult:
    def __init__(self, id: int, front_rank: int, crowding_distance_value: float):
        self.id = id
        self.front_rank = front_rank
        self.crowding_distance_value = crowding_distance_value


class NSGA3:
    def run_generation(self, uavs: [UAV], selected_objectives: [OptimizationObjective], crossover_rate: float, mutation_rate: float):
        objectives = []
        for uav in uavs:
            objective_values = [0] * len(selected_objectives)
            for objective_id in range(len(selected_objectives)):
                objective_values[objective_id] = self.objective_function(uav, selected_objectives[objective_id])
            objectives.append(objective_values)

        # Non-dominated sorting
        fronts = self.non_dominated_sort(objectives)
        # Crowding distance calculation
        crowding_distances = []
        for f in range(len(fronts)):
            crowding_distances += self.crowding_distance_assignment(fronts[f], objectives, f)

        new_population = []
        while len(new_population) < len(uavs):
            # Tournament selection
            parent1 = self.tournament_selection(uavs, crowding_distances)
            parent2 = self.tournament_selection(uavs, crowding_distances)

            # Crossover
            offspring_genes = self.crossover(parent1, parent2, crossover_rate)

            # Mutation
            mutated_genes = self.mutate(offspring_genes, mutation_rate)

            new_population.append(UAV(
                Genotype(mutated_genes),
                uavs[0].map
            ))
        return new_population

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
        fronts = [[]]

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
                fronts[0].append(i)

        # Step 3: Fronts Construction
        index = 0
        while len(fronts[index]) > 0:
            next_front = []

            for i in fronts[index]:
                for j in range(population_size):
                    if dominance_matrix[j][i] == 1:
                        ranks[j] -= 1

                        if ranks[j] == 0:
                            next_front.append(j)

            index += 1
            fronts.append(next_front)

        fronts.pop()
        fronts.reverse()
        # The fronts list contains a list of fronts, where each front is represented by a list of indices corresponding
        # to solutions in that front. The fronts are ordered based on dominance relationships, with the first front
        # containing non-dominated solutions, and so on.
        return fronts

    # Crowding distance assignment
    @staticmethod
    def crowding_distance_assignment(front, objectives, front_rank):
        population_size = len(front)
        distances = [0] * population_size
        for objective_index in range(len(objectives[0])):
            # sort by current objective value
            front = sorted(front, key=lambda x: objectives[x][objective_index])
            distances[0] = math.inf
            distances[population_size - 1] = math.inf

            objective_min = objectives[front[0]][objective_index]
            objective_max = objectives[front[population_size - 1]][objective_index]

            if objective_max == objective_min:
                continue

            for i in range(1, population_size - 1):
                distances[i] += (objectives[front[i + 1]][objective_index] - objectives[front[i - 1]][objective_index]) \
                                / (objective_max - objective_min)

        # Associate distances with UAV and objective IDs
        return [CrowdingDistanceResult(front[i], distances[i], front_rank) for i in range(population_size)]

    @staticmethod
    def dominates(objective_values1, objective_values2):
        # Check if objective_values1 dominates objective_values2
        # Returns True if objective_values1 dominates objective_values2, False otherwise
        return all(o1 <= o2 for o1, o2 in zip(objective_values1, objective_values2))

    @staticmethod
    def tournament_selection(uavs, crowding_distances, tournament_size=2):
        # tournament selection
        tournament_indices = random.sample(range(len(uavs)), tournament_size)

        # Select the UAV with the smaller front rank, and if equal, select the one with the smaller crowding distance
        winner_index = min(tournament_indices, key=lambda idx: (crowding_distances[idx].front_rank, crowding_distances[idx].crowding_distance_value))

        return uavs[winner_index]

    @staticmethod
    def crossover(parent1: UAV, parent2: UAV, crossover_rate: float):
        genes1 = parent1.genotype.move_genes
        genes2 = parent2.genotype.move_genes

        assert len(genes1) == len(genes2), "Parent genes must have the same length"

        if random.random() <= crossover_rate:
            # random crossover point
            crossover_point = random.randint(0, len(genes1) - 1)

            # combining genes from both parents
            offspring_genes = genes1[:crossover_point] + genes2[crossover_point:]
            return offspring_genes
        else:
            return genes1 if random.random() < 0.5 else genes2

    @staticmethod
    def mutate(genes: [MoveGene], mutation_rate):
        mutated_genes = genes

        if random.random() <= mutation_rate:
            num_genes = len(genes)
            num_genes_to_mutate = int(mutation_rate * num_genes) + 1  # Ensure at least one gene is mutated
            selected_gene_indices = random.sample(range(num_genes), num_genes_to_mutate)
            for i in selected_gene_indices:
                mutated_genes[i] = MoveGene(random.randint(0, 7))

        return mutated_genes
