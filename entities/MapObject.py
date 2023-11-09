from enum import Enum
from entities.Point2d import Point2d

class MapObjectType(Enum):
    START = 0
    OBJECTIVE = 1
    OBSTACLE = 2
    UAV = 3


class MapObject:
    def __init__(self, position: Point2d, radius: int, object_type: MapObjectType):
        self.position = position
        self.radius = radius
        self.type = object_type

    def set_type(self, new_type: MapObjectType):
        self.type = new_type

    def get_type(self):
        return self.type

    def is_point_inside(self, point: Point2d):
        return self.position.count_distance(point) <= self.radius

    def does_move_intercourse_obstacle(self, p1, p2):
        segment_to_object_center_distance = Point2d.distance_segment_to_point(p1, p2, self.position)
        return segment_to_object_center_distance <= self.radius
