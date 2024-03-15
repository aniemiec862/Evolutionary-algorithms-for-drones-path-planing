import random
from abc import ABC

from evolution.objective import OptimizationObjective
from genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from map.map import Map
from uav.genotype import Genotype
from uav.uav import UAV


class ObjectiveUav:
    def __init__(self, id: int, objectives, encountered_obstacles: int):
        self.id = id
        self.objectives = objectives
        self.encountered_obstacles = encountered_obstacles

class FrontUav:
    def __init__(self, id: int, front_rank: int = None):
        self.id = id
        self.front_rank = front_rank

class NSGA3(GeneticAlgorithm, ABC):
    def __init__(self, selected_objectives: [OptimizationObjective], crossover_rate: float, mutation_rate: float,
                 map: Map, evaluate_whole_population: bool):
        super().__init__(selected_objectives, crossover_rate, mutation_rate, map)
        self.evaluate_whole_population = evaluate_whole_population

    def run_generation(self, uavs: [UAV]):
        objectives = self.calculate_objective_values(uavs)
        fronts = self.create_fronts_by_obstacles(objectives)
        best_uavs_number = 0.3 * len(uavs)

        parents = []
        for front_id in range(len(fronts)):
            if len(parents) == best_uavs_number:
                break
            for id in fronts[front_id]:
                parents.append(FrontUav(id, front_id))
                if len(parents) == best_uavs_number:
                    break

        children = []
        while len(children) < len(uavs):
            # Tournament selection
            parent1_id = self.tournament_selection(parents)
            parent2_id = parent1_id
            while parent2_id == parent1_id:
                parent2_id = self.tournament_selection(parents)

            parent1 = uavs[parent1_id]
            parent2 = uavs[parent2_id]

            # Crossover
            offspring_genes = self.crossover(parent1, parent2, self.crossover_rate)
            uav = UAV(Genotype(offspring_genes, parent1.genotype.start_position, parent1.genotype.subobjectives), self.map)

            # Mutation
            self.mutate(uav, self.mutation_rate)

            uav.genotype.add_subjectives()
            uav.genotype.sort_by_distance()

            children.append(uav)

        if self.evaluate_whole_population:
            whole_population = uavs + children
            ranked_uavs = self.rank_uavs(whole_population)
            return ranked_uavs[:len(uavs)]
        else:
            return children

    def calculate_objective_values(self, uavs):
        objectives = []
        for id, uav in enumerate(uavs):
            objective_values = [0] * len(self.selected_objectives)
            for objective_id in range(len(self.selected_objectives)):
                objective_values[objective_id] = self.objective_function(uav, self.selected_objectives[objective_id])
            objectives.append(ObjectiveUav(id, objective_values, self.objective_function(uav, OptimizationObjective.ENCOUNTERED_OBSTACLES)))
        return objectives

    def rank_uavs(self, uavs: [UAV]):
        objectives = self.calculate_objective_values(uavs)
        fronts = self.create_fronts_by_obstacles(objectives)

        new_population = []
        for front in fronts:
            new_len = len(new_population) + len(front)

            if new_len < (len(uavs) / 2):
                new_population += front
            elif new_len <= (len(uavs) / 2):
                new_population += front
                break
            else:
                missing_no_uavs = new_len - (len(uavs) / 2)
                new_population += self.assign_reference_points(uavs, objectives, new_population, front, missing_no_uavs)

        new_population = list(map(lambda id: uavs[id], new_population))
        return new_population

    def assign_reference_points(self, uavs, objectives, new_population, front, missing_no_uavs):
        # [[val_min, mid, val_max], [val_min, mid, val_max], [val_min, mid, val_max]]
        grid_intervals = self.split_space(objectives)
        # counted_points = [
        #     [1, 0, 5],  # Objective 1
        #     [0, 2, 4]  # Objective 2
        # ]
        counted_points = self.assign_population_to_grid(grid_intervals, new_population, uavs)

        # Combine counts with intervals
        intervals_with_counts = [(obj_id, interval_idx, count)
                                 for obj_id, counts in enumerate(counted_points)
                                 for interval_idx, count in enumerate(counts)]
        sorted_intervals = sorted(intervals_with_counts, key=lambda x: x[2])

        uavs_assigned_to_min_count_intervals = []
        for obj_id, interval_idx, _ in sorted_intervals:
            if len(uavs_assigned_to_min_count_intervals) == missing_no_uavs:
                break
            for uav_id in front:
                uav = uavs[uav_id]
                obj_value = self.objective_function(uav, objectives[obj_id])
                interval = grid_intervals[obj_id][interval_idx]
                if obj_value >= interval:
                    uavs_assigned_to_min_count_intervals.append(uav_id)
                    break

        return uavs_assigned_to_min_count_intervals

    @staticmethod
    def split_space(objectives):
        grid_density = 10
        min_values = [min(column) for column in zip(*objectives)]
        max_values = [max(column) for column in zip(*objectives)]

        grid_density = [grid_density] * len(min_values)

        # Calculate step sizes for each dimension
        step_sizes = [(max_val - min_val) / num_part for min_val, max_val, num_part in
                      zip(min_values, max_values, grid_density)]

        # Generate evenly spaced intervals along each dimension
        intervals = [[min_val + i * step_size for i in range(num_part + 1)] for min_val, step_size, num_part in
                     zip(min_values, step_sizes, grid_density)]

        return intervals

    def assign_population_to_grid(self, intervals, new_population, uavs):
        objectives_count = [[0 for _ in range(len(intervals[0]) - 1)] for _ in range(len(self.selected_objectives))]

        for uav_id in new_population:
            uav = uavs[uav_id]
            for obj_id, objective in enumerate(self.selected_objectives):
                obj_value = self.objective_function(uav, objective)
                for interval_id, interval in enumerate(intervals[obj_id]):
                    if obj_value >= interval:
                        objectives_count[obj_id][interval_id] += 1
                        break

        return objectives_count

    def create_fronts_by_obstacles(self, uavs: [FrontUav]):
        sorted_by_obstacles = sorted(uavs, key=lambda x: x.encountered_obstacles)

        global_fronts = []
        current_obstacle_front_uavs = []
        current_key = uavs[0].encountered_obstacles

        for uav in sorted_by_obstacles:
            uav_objective = uav.encountered_obstacles
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

    @staticmethod
    def dominates(objective_values1, objective_values2):
        # Returns True if objective_values1 dominates objective_values2, False otherwise
        return all(o1 <= o2 for o1, o2 in zip(objective_values1, objective_values2))

    @staticmethod
    def tournament_selection(parents):
        # tournament selection
        tournament_indices = random.sample(range(len(parents)), 2)

        parent1 = parents[tournament_indices[0]]
        parent2 = parents[tournament_indices[1]]

        return parent1.id if parent1.front_rank < parent2.front_rank else parent2.id

    @staticmethod
    def crossover(parent1: UAV, parent2: UAV, crossover_rate: float):
        genes1 = parent1.genotype
        genes2 = parent2.genotype

        if random.random() <= crossover_rate:
            return genes1.crossover(genes2)
        else:
            return genes1.position_genes if random.random() < 0.5 else genes2.position_genes

    def mutate(self, uav: UAV, mutation_rate):
        if random.random() <= mutation_rate:
            uav.genotype.mutate(self.map)
