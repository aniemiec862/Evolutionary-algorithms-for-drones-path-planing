from abc import abstractmethod, ABC

from evolution.objective import OptimizationObjective
from map.map import Map
from uav.uav import UAV


class GeneticAlgorithm(ABC):
    @abstractmethod
    def __init__(self, selected_objectives: [OptimizationObjective], crossover_rate: float, mutation_rate: float, map: Map):
        self.selected_objectives = selected_objectives
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.map = map

    @abstractmethod
    def run_generation(self, uavs: [UAV]):
        pass

    def objective_function(self, uav: UAV, objective: OptimizationObjective):
        if objective == OptimizationObjective.PATH_SCORE:
            return uav.get_cost()

        if objective == OptimizationObjective.ENCOUNTERED_OBSTACLES:
            return uav.intersection_moves

        if objective == OptimizationObjective.PATH_LENGTH:
            return uav.path_length

        if objective == OptimizationObjective.PATH_SMOOTHNESS:
            return uav.calculate_path_smoothness()

        if objective == OptimizationObjective.OBSTACLE_PROXIMITY:
            return uav.obstacle_proximity
