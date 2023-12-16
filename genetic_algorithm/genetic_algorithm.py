from abc import abstractmethod, ABC

from evolution.objective import OptimizationObjective
from uav.uav import UAV
from utils.Point2d import Point2d


class GeneticAlgorithm(ABC):
    @abstractmethod
    def __init__(self, selected_objectives: [OptimizationObjective], crossover_rate: float, mutation_rate: float, max_position: Point2d):
        self.selected_objectives = selected_objectives
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.max_position = max_position

    @abstractmethod
    def run_generation(self, uavs: [UAV]):
        pass
