import string

from genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from map.map import Map
from map.map_object import MapUAV, MapObject
from uav.genotype import Genotype
from uav.uav import UAV
from utils import constants


class EvolutionEngine:
    def __init__(self, no_uavs: int, no_generations: int, map: Map, max_moves_length: int, visualize_all_steps: bool):
        self.uavs = []
        self.no_uavs = no_uavs
        self.no_generations = no_generations
        self.map = map
        self.max_moves_length = max_moves_length
        self.visualize_all_steps = visualize_all_steps
        constants.final_uavs = []

    def init_uavs(self, subobjectives: list[MapObject]):
        uavs = []
        for _ in range(self.no_uavs):
            genotype = Genotype.generate_random_with_sorted_by_distance(self.max_moves_length, self.map.start.position, self.map.objective.position, subobjectives)
            uavs.append(UAV(genotype, self.map))
        self.uavs = uavs

    def run(self, algorithm: GeneticAlgorithm):
        for gen_id in range(self.no_generations):
            print("Gen: ", gen_id + 1)
            self.run_generation(gen_id, algorithm)

        constants.final_uavs += self.uavs[:1]

        if self.visualize_all_steps is False:
            self.visualize_uavs(algorithm.get_name(), self.no_generations, False)

    def run_generation(self, gen_id, algorithm: GeneticAlgorithm):
        for uav in self.uavs:
            uav.move()

        if self.visualize_all_steps is True:
            self.visualize_uavs(algorithm.get_name(), gen_id + 1, False)

        if gen_id + 1 == self.no_generations:
            return

        self.uavs = algorithm.run_generation(self.uavs)

    def visualize_uavs(self, algorithm_name: string, generation_id: int, is_final_result: bool):
        if is_final_result:
            uavs = [MapUAV(uav.get_moves(), uav.calculate_traveled_distance()) for uav in constants.final_uavs]
        else:
            uavs = [MapUAV(uav.get_moves(), uav.calculate_traveled_distance()) for uav in self.uavs[:1]]
        self.map.visualize(algorithm_name, generation_id, uavs)

    def print_uavs(self):
        for uav in self.uavs:
            coordinates = [(point.x, point.y) for point in uav.genotype.position_genes]
            print(coordinates)
