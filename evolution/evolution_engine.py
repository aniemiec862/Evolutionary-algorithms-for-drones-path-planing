from genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from genetic_algorithm.spea2 import SPEA2
from map.map import Map
from map.map_object import MapUAV
from uav.genotype import Genotype
from uav.uav import UAV


class EvolutionEngine:
    def __init__(self, no_uavs: int, no_generations: int, map: Map, max_moves_length: int, visualize_all_steps: bool):
        self.uavs = self.init_uavs(no_uavs, map, max_moves_length)
        self.no_generations = no_generations
        self.map = map
        self.max_moves_length = max_moves_length
        self.visualize_all_steps = visualize_all_steps

    @staticmethod
    def init_uavs(no_uavs: int, map: Map, moves_length: int):
        uavs = []
        for _ in range(no_uavs):
            # genotype = Genotype.generate_random(moves_length, map.width, map.height)
            genotype = Genotype.generate_random_with_sorted_by_distance(moves_length, map.start.position, map.objective.position)
            uavs.append(UAV(genotype, map))
        return uavs

    def run(self, algorithm: GeneticAlgorithm):
        for gen_id in range(self.no_generations):
            print("Gen: ", gen_id + 1)
            self.run_generation(gen_id, algorithm)

        if self.visualize_all_steps is False:
            self.visualize_uavs(algorithm, self.no_generations)

    def run_generation(self, gen_id, algorithm: GeneticAlgorithm):
        for uav in self.uavs:
            uav.move()

        if self.visualize_all_steps is True:
            self.visualize_uavs(algorithm, gen_id + 1)

        if gen_id + 1 == self.no_generations:
            return

        self.uavs = algorithm.run_generation(self.uavs)

    def visualize_uavs(self, algorithm: GeneticAlgorithm, generation_id: int):
        alg_name = "SPEA2" if isinstance(algorithm, SPEA2) else "NSGA3"
        self.map.visualize(alg_name, generation_id, self.get_map_uavs())

    def get_map_uavs(self):
        sorted_uav_list = sorted(self.uavs, key=lambda uav: uav.get_cost())
        return [MapUAV(uav.get_moves(), uav.calculate_traveled_distance()) for uav in sorted_uav_list[:1]]

    def print_uavs(self):
        for uav in self.uavs:
            coordinates = [(point.x, point.y) for point in uav.genotype.position_genes]
            print(coordinates)
