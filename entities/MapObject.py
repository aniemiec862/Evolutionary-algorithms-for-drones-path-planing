from enum import Enum
from entities.Point2d import Point2d


class MapObjectType(Enum):
    START = 0
    OBJECTIVE = 1
    OBSTACLE = 2
    UAV = 3

class MapObject:
    def __init__(self, position: Point2d, radius: int, type: MapObjectType):
        self.position = position
        self.radius = radius
        self.type = type

    def set_type(self, new_type: MapObjectType):
        self.type = new_type

    def get_type(self):
        return self.type

    def is_point_inside(self, point: Point2d):
        return self.position.count_distance(point) <= self.radius

    def does_move_intercourse_obstacle(self, p1, p2):
        # y = mx + b
        m = (p2.y - p1.y) / (p2.x - p1.x)
        b = p1.y - m*p1.x

        #(1 + m^2)x^2 + 2bmx + b^2 – r^2 = 0
        delta = (2*b*m)**2 - 4*(1+m**2)*(b**2-self.radius**2)
        return delta < 0
