import random
from math import sqrt
import numpy as np

from utils import constants
from utils.Point2d import Point2d


class Point3d:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def count_distance(self, point):
        return sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2)

    def count_distance_flat(self, point):
        return sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    @staticmethod
    def is_position_between_valid_range(point):
        def is_between_range(value, max_value):
            return 0 <= value <= max_value

        return is_between_range(point.x, constants.max_width) and is_between_range(point.y, constants.max_depth) and is_between_range(point.z, constants.max_height)

    @staticmethod
    def calculate_angle(pos1, pos2, pos3):
        # Calculate the angle between three positions
        vector1 = np.array([pos1.x - pos2.x, pos1.y - pos2.y])
        vector2 = np.array([pos3.x - pos2.x, pos3.y - pos2.y])

        dot_product = np.dot(vector1, vector2)
        norm_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)

        if norm_product == 0:
            return 0.0

        cos_angle = dot_product / norm_product
        return np.arccos(np.clip(cos_angle, -1.0, 1.0))
