import math
import random
from abc import ABC

from evolution.objective import OptimizationObjective
from genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from map.map import Map
from uav.genotype import Genotype
from uav.uav import UAV


class CrowdingDistanceResult:
    def __init__(self, id: int, front_rank: int, crowding_distance_value: float):
        self.id = id
        self.front_rank = front_rank
        self.crowding_distance_value = crowding_distance_value


class NSGA3(GeneticAlgorithm, ABC):
    def __init__(self, selected_objectives: [OptimizationObjective], crossover_rate: float, mutation_rate: float, map: Map):
        super().__init__(selected_objectives, crossover_rate, mutation_rate, map)

    def run_generation(self, uavs: [UAV]):
        objectives = []
        for uav in uavs:
            objective_values = [0] * len(self.selected_objectives)
            for objective_id in range(len(self.selected_objectives)):
                objective_values[objective_id] = self.objective_function(uav, self.selected_objectives[objective_id])
            objectives.append(objective_values)

        # Non-dominated sorting
        fronts = self.non_dominated_sort(objectives)

        # reference_points = self.generate_reference_points(len(self.selected_objectives), len(uavs))

        # Crowding distance calculation
        crowding_distances = []
        for f in range(len(fronts)):
            crowding_distances += self.crowding_distance_assignment(fronts[f], objectives, f)

        new_population = []
        while len(new_population) < len(uavs):
            # Tournament selection
            parent1_id = self.tournament_selection(uavs, crowding_distances)
            parent2_id = parent1_id
            while parent2_id == parent1_id:
                parent2_id = self.tournament_selection(uavs, crowding_distances)

            parent1 = uavs[parent1_id]
            parent2 = uavs[parent2_id]

            # Crossover
            offspring_genes = self.crossover(parent1, parent2, self.crossover_rate)
            uav = UAV(Genotype(offspring_genes, parent1.genotype.start_position), uavs[0].map)

            # Mutation
            self.mutate(uav, self.mutation_rate)

            uav.genotype.sort_by_distance()

            new_population.append(uav)
        return new_population

    @staticmethod
    def objective_function(uav: UAV, objective: OptimizationObjective):
        # Example: Assume a bi-objective optimization problem
        # where we aim to minimize two objectives: f1 and f2

        # # Objective 1: Minimize f1
        if objective == OptimizationObjective.PATH_SCORE:
            f1 = uav.get_cost()
            return f1

        # Objective 2: Minimize f2
        # if objective == OptimizationObjective.TRAVELED_DISTANCE:
        #     f2 = uav.get_cost()
        #     return f2

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

    @staticmethod
    def generate_reference_points(num_objectives, num_reference_points):
        return [[random.uniform(0, 1) for _ in range(num_objectives)] for _ in range(num_reference_points)]

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
        return [CrowdingDistanceResult(front[i], front_rank, distances[i]) for i in range(population_size)]

    @staticmethod
    def dominates(objective_values1, objective_values2):
        # Returns True if objective_values1 dominates objective_values2, False otherwise
        return all(o1 <= o2 for o1, o2 in zip(objective_values1, objective_values2))

    @staticmethod
    def tournament_selection(uavs, crowding_distances, tournament_size=2):
        # tournament selection
        tournament_indices = random.sample(range(len(uavs)), tournament_size)

        # Select the UAV with smaller front rank, and if equal, select the one with the smaller crowding distance
        winner_index = min(tournament_indices, key=lambda idx: (crowding_distances[idx].front_rank, crowding_distances[idx].crowding_distance_value))
        return winner_index

    @staticmethod
    def crossover(parent1: UAV, parent2: UAV, crossover_rate: float):
        genes1 = parent1.genotype
        genes2 = parent2.genotype

        assert len(genes1.position_genes) == len(genes2.position_genes), "Parent genes must have the same length"

        if random.random() <= crossover_rate:
            return genes1.crossover(genes2)
        else:
            return genes1.position_genes if random.random() < 0.5 else genes2.position_genes

    @staticmethod
    def mutate(uav: UAV, mutation_rate):
        if random.random() <= mutation_rate:
            uav.genotype.mutate(uav.map)
