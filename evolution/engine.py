from genetic_algorithm.genetic_algorithm import OptimizationObjective
from genetic_algorithm.nsga3 import NSGA3
from map.map import Map
from uav.genotype import Genotype
from uav.uav import UAV


class Engine:
    def __init__(self, no_uavs: int, no_generations: int, map: Map, max_moves_length: int, ):
        self.uavs = self.init_uavs(no_uavs, map, max_moves_length)
        self.no_generations = no_generations
        self.max_moves_length = max_moves_length

    @staticmethod
    def init_uavs(no_uavs: int, map: Map, moves_length: int):
        uavs = []
        for _ in range(no_uavs):
            genotype = Genotype.generate_random(moves_length)
            uavs.append(UAV(genotype, map))
        return uavs

    def run(self):
        for gen_id in range(self.no_generations):
            self.run_generation(gen_id)

    def run_generation(self, gen_id):
        for _ in range(self.max_moves_length):
            self.move_uavs()

        if gen_id + 1 == self.no_generations:
            return

        self.uavs = NSGA3().run_generation(
            self.uavs,
            [OptimizationObjective.TRAVELED_DISTANCE, OptimizationObjective.DISTANCE_FROM_OBJECTIVE],
            0.9,
            0.1 / len(self.uavs),
        )

    def move_uavs(self):
        for uav in self.uavs:
            if not uav.is_destroyed and not uav.has_reach_objective:
                uav.move()
