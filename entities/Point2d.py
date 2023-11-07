from math import sqrt

class Point2d:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def count_distance(self, point):
        return sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)
