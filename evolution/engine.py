from genetic_algorithm.genetic_algorithm import OptimizationObjective
from genetic_algorithm.nsga3 import NSGA3
from map.map import Map
from map.map_object import MapUAV
from uav.genotype import Genotype
from uav.uav import UAV


class Engine:
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
            genotype = Genotype.generate_random(moves_length)
            uavs.append(UAV(genotype, map))
        return uavs

    def run(self):
        for gen_id in range(self.no_generations):
            print("Gen: ", gen_id + 1)
            self.run_generation(gen_id)

        if self.visualize_all_steps is False:
            self.visualize_uavs(self.no_generations)

    def run_generation(self, gen_id):
        for _ in range(self.max_moves_length):
            self.move_uavs()

        if self.visualize_all_steps is True:
            self.visualize_uavs(gen_id + 1)

        if gen_id + 1 == self.no_generations:
            return

        self.uavs = NSGA3().run_generation(
            self.uavs,
            [OptimizationObjective.DISTANCE_FROM_OBJECTIVE],
            0.9,
            0.1 / len(self.uavs),
        )

    def move_uavs(self):
        for uav in self.uavs:
            if not uav.is_destroyed and not uav.has_reach_objective:
                uav.move()

    def visualize_uavs(self, generation_id: int):
        list_of_map_uavs = [MapUAV(uav.get_moves(), uav.calculate_traveled_distance()) for uav in self.uavs]
        self.map.visualize(generation_id, list_of_map_uavs)

    def print_uavs(self):
        for uav in self.uavs:
            print(uav.genotype.move_genes)
