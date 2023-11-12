from map.map import Map
from uav.genotype import Genotype
from uav.uav import UAV


class Engine:
    def __init__(self, no_uavs: int, no_iterations: int, map: Map, max_moves_length: int,):
        self.uavs = self.init_uavs(no_uavs, map, max_moves_length)
        self.no_iterations = no_iterations
        self.max_moves_length = max_moves_length

    @staticmethod
    def init_uavs(no_uavs: int, map: Map, moves_length: int):
        uavs = []
        for _ in range(no_uavs):
            genotype = Genotype.generate_random(moves_length)
            uavs.append(UAV(genotype, map))
        return uavs

    def run(self):
        for _ in range(self.no_iterations):
            self.reset()
            self.run_iteration()

    def run_iteration(self):
        for _ in range(self.max_moves_length):
            self.move_uavs()

    def move_uavs(self):
        for uav in self.uavs:
            if not uav.is_destroyed and not uav.has_reach_objective:
                uav.move()

    def reset(self):
        for uav in self.uavs:
            uav.reset()
