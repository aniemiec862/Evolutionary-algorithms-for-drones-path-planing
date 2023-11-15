from abc import ABC, abstractmethod
from enum import Enum

class OptimizationObjective(Enum):
    TRAVELED_DISTANCE = 0
    DISTANCE_FROM_OBJECTIVE = 1

# class GeneticAlgorithm(ABC):
#
#     @abstractmethod
#     def selection(self):
#         pass
#
#     @abstractmethod
#     def crossover(self):
#         pass
#
#     @abstractmethod
#     def mutation(self):
#         pass
