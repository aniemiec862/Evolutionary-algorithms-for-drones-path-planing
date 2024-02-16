from enum import Enum


class OptimizationObjective(Enum):
    PATH_SCORE = 0,
    ENCOUNTERED_OBSTACLES = 1,
    PATH_LENGTH = 2,
    PATH_SMOOTHNESS = 3,
    OBSTACLE_PROXIMITY = 4

