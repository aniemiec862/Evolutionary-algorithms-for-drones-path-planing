import math
import random
from abc import ABC

from evolution.objective import OptimizationObjective
from genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from map.map import Map
from uav.genotype import Genotype
from uav.uav import UAV


class UAVFitness:
    def __init__(self, uav: UAV, fitness: float):
        self.uav = uav
        self.fitness = fitness


class SPEA2(GeneticAlgorithm, ABC):
    def __init__(self, selected_objectives: [OptimizationObjective], crossover_rate: float, mutation_rate: float,
                 map: Map, init_uavs: [UAV], archive_size: int):
        super().__init__(selected_objectives, crossover_rate, mutation_rate, map)
        self.archive_size = archive_size
        self.archive = []
        self.update_archive(init_uavs)

    def run_generation(self, uavs: [UAV]):
        new_population = []
        while len(new_population) < len(uavs) - self.archive_size:
            # Tournament selection
            parent1_id = self.tournament_selection()
            parent2_id = parent1_id
            while parent2_id == parent1_id:
                parent2_id = self.tournament_selection()

            parent1 = self.archive[parent1_id].uav
            parent2 = self.archive[parent2_id].uav

            # Crossover
            offspring_genes = self.crossover(parent1, parent2, self.crossover_rate)
            uav = UAV(Genotype(offspring_genes, parent1.genotype.start_position), self.map)

            # Mutation
            self.mutate(uav, self.mutation_rate)
            uav.genotype.sort_by_distance()

            new_population.append(uav)

        new_population += [item.uav for item in self.archive]
        self.update_archive(new_population)
        return new_population

    def calculate_fitness(self, uavs: [UAV]):
        raw_fitness = self.calculate_raw_fitness(uavs)
        k_neighbour = math.floor(math.sqrt(len(uavs) + self.archive_size))
        density = self.calculate_density(uavs, k_neighbour)

        fitness = [0 for _ in range(len(uavs))]
        for i in range(len(uavs)):
            fitness[i] = raw_fitness[i] + density[i]

        fitness_uavs = []
        for i in range(len(uavs)):
            fitness_uavs.append(UAVFitness(uavs[i], fitness[i]))
        return fitness_uavs

    def calculate_raw_fitness(self, uavs: [UAV]):
        # raw fitness of solution i is a summation of strength of solutions dominating i
        strength = [0 for _ in range(len(uavs))]
        raw_fitness = [0 for _ in range(len(uavs))]

        for i in range(len(uavs)):
            for j in range(len(uavs)):
                if i != j and self.dominates(uavs[i], uavs[j]):
                    strength[i] += 1

        for i in range(len(uavs)):
            for j in range(len(uavs)):
                if i != j and self.dominates(uavs[i], uavs[j]):
                    raw_fitness[j] += strength[i]

        return raw_fitness

    def dominates(self, uav1, uav2):
        count = 0
        for objective in self.selected_objectives:
            if self.objective_function(uav1, objective) <= self.objective_function(uav2, objective):
                count += 1
        return count == len(self.selected_objectives)

    def calculate_density(self, uavs: [UAV], k_neighbour: int):
        distance = [[0] * len(uavs) for _ in range(len(uavs))]
        density = [0 for _ in range(len(uavs))]

        for i in range(len(uavs)):
            for j in range(len(uavs)):
                if i != j:
                    distance[i][j] = self.euclidean_distance(uavs[i], uavs[j])
            ordered_distances = sorted(distance[i])[1:]
            density[i] = 1 / (ordered_distances[k_neighbour] + 2)

        return density

    def euclidean_distance(self, uav1, uav2):
        distance = 0
        for objective in self.selected_objectives:
            distance += (self.objective_function(uav1, objective) - self.objective_function(uav2, objective)) ** 2
        return math.sqrt(distance)

    def update_archive(self, new_population: [UAV]):
        for uav in new_population:
            uav.move()

        fitness_uavs = self.calculate_fitness(new_population)
        fitness_uavs_ordered = sorted(fitness_uavs, key=lambda fitness_uav: (fitness_uav.uav.intersection_moves, fitness_uav.fitness))
        self.archive = fitness_uavs_ordered[:self.archive_size]

    def tournament_selection(self, tournament_size=2):
        # tournament selection
        tournament_indices = random.sample(range(len(self.archive)), tournament_size)

        # Select the UAV with smaller fitness, and if equal, select the one with the smaller crowding distance
        winner_index = min(tournament_indices, key=lambda idx: self.archive[idx].fitness)
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

    def mutate(self, uav: UAV, mutation_rate):
        if random.random() <= mutation_rate:
            uav.genotype.mutate(self.map)
