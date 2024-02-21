import math
import random
from abc import ABC

from evolution.objective import OptimizationObjective
from genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from map.map import Map
from uav.genotype import Genotype
from uav.uav import UAV

class ObjectiveUav:
    def __init__(self, id: int, objectives):
        self.id = id
        self.objectives = objectives

class CrowdingDistanceResult:
    def __init__(self, id: int, front_rank: int, crowding_distance_value: float):
        self.id = id
        self.front_rank = front_rank
        self.crowding_distance_value = crowding_distance_value


class NSGA2(GeneticAlgorithm, ABC):
    def __init__(self, selected_objectives: [OptimizationObjective], crossover_rate: float, mutation_rate: float, map: Map, evaluate_whole_population: bool):
        super().__init__(selected_objectives, crossover_rate, mutation_rate, map)
        self.evaluate_whole_population = evaluate_whole_population

    def run_generation(self, uavs: [UAV]):
        crowding_distances = self.rank_uavs(uavs, True)
        crowding_distances = crowding_distances[:int(0.3*len(crowding_distances))]

        children = []
        while len(children) < len(uavs):
            # Tournament selection
            parent1_id = self.tournament_selection(crowding_distances)
            parent2_id = parent1_id
            while parent2_id == parent1_id:
                parent2_id = self.tournament_selection(crowding_distances)

            parent1 = uavs[parent1_id]
            parent2 = uavs[parent2_id]

            # Crossover
            offspring_genes = self.crossover(parent1, parent2, self.crossover_rate)
            uav = UAV(Genotype(offspring_genes, parent1.genotype.start_position), self.map)

            # Mutation
            self.mutate(uav, self.mutation_rate)

            uav.genotype.sort_by_distance()

            children.append(uav)

        if self.evaluate_whole_population:
            whole_population = uavs + children
            crowding_distances = self.rank_uavs(whole_population, False)

            new_population = []
            for cd in crowding_distances[:len(uavs)]:
                uav = whole_population[cd.id]
                new_population.append(uav)

            return new_population
        else:
            return children

    def rank_uavs(self, uavs: [UAV], calculate_all_distances: bool):
        objectives = []
        objectives_uavs = []
        for id, uav in enumerate(uavs):
            objective_values = [0] * len(self.selected_objectives)
            for objective_id in range(len(self.selected_objectives)):
                objective_values[objective_id] = self.objective_function(uav, self.selected_objectives[objective_id])
            objectives.append(objective_values)
            objectives_uavs.append(ObjectiveUav(id, objective_values))

        fronts = self.create_fronts_by_obstacles(objectives_uavs)

        # Crowding distance calculation
        crowding_distances = []
        for f in range(len(fronts)):
            crowding_distances += self.crowding_distance_assignment(fronts[f], objectives, f)
            if calculate_all_distances is False and len(crowding_distances) >= (len(uavs) / 2):
                break

        return crowding_distances

    def create_fronts_by_obstacles(self, uavs: [ObjectiveUav]):
        sorted_by_obstacles = sorted(uavs, key=lambda x: x.objectives[0])

        global_fronts = []
        current_obstacle_front_uavs = []
        current_key = uavs[0].objectives[0]

        for uav in sorted_by_obstacles:
            uav_objective = uav.objectives[0]
            if uav_objective != current_key:
                if current_obstacle_front_uavs:
                    global_fronts.append(self.process_front(current_obstacle_front_uavs))
                current_key = uav_objective
                current_obstacle_front_uavs = [uav]
            else:
                current_obstacle_front_uavs.append(uav)

        if current_obstacle_front_uavs:
            global_fronts.append(self.process_front(current_obstacle_front_uavs))

        flattened_result = [inner_list for outer_list in global_fronts for inner_list in outer_list]

        return flattened_result

    def process_front(self, current_obstacle_front_uavs):
        current_obstacle_front_objectives = [uav.objectives for uav in current_obstacle_front_uavs]
        current_obstacle_fronts = self.non_dominated_sort(current_obstacle_front_objectives)
        current_obstacle_front_mapped_to_uavs_ids = [[current_obstacle_front_uavs[id].id for id in front] for front in
                                                     current_obstacle_fronts]
        return current_obstacle_front_mapped_to_uavs_ids

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
        return [CrowdingDistanceResult(front[i], front_rank, distances[i]) for i in range(population_size)]

    @staticmethod
    def dominates(objective_values1, objective_values2):
        # Returns True if objective_values1 dominates objective_values2, False otherwise
        return all(o1 <= o2 for o1, o2 in zip(objective_values1, objective_values2))

    @staticmethod
    def tournament_selection(crowding_distances, tournament_size=2):
        # tournament selection
        tournament_indices = random.sample(range(len(crowding_distances)), tournament_size)

        # Select the UAV with smaller front rank, and if equal, select the one with the smaller crowding distance
        winner_index = min(tournament_indices, key=lambda idx: (crowding_distances[idx].front_rank, crowding_distances[idx].crowding_distance_value))
        return crowding_distances[winner_index].id

    @staticmethod
    def crossover(parent1: UAV, parent2: UAV, crossover_rate: float):
        genes1 = parent1.genotype
        genes2 = parent2.genotype

        assert len(genes1.position_genes) == len(genes2.position_genes), "Parent genes must have the same length"

        if random.random() <= crossover_rate:
            return genes1.crossover(genes2)
        else:
            return genes1.position_genes if random.random() < 0.5 else genes2.position_genes

    def mutate(self, uav: UAV, mutation_rate):
        if random.random() <= mutation_rate:
            uav.genotype.mutate(self.map)
