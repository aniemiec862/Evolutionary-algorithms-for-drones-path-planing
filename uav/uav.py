from utils.Point2d import Point2d
from map.map import Map
from uav.genotype import Genotype
import math


class UAV:
    def __init__(self, genotype: Genotype, map: Map):
        self.genotype = genotype
        self.map = map
        self.start = map.start
        self.objective = map.objective
        self.obstacles = map.obstacles
        self.position = self.start.position
        self.moves = [self.start.position] + genotype.position_genes + [self.objective.position]
        self.intersection_moves = 0
        self.obstacle_proximity = 0
        self.cost = 0

    def move(self):
        for move_id in range(1, len(self.moves)):
            new_position = self.moves[move_id]
            if not self.validate_can_move_to_position(new_position):
                self.intersection_moves += 1
            self.calculate_obstacle_proximity()
            self.position = new_position

        self.calculate_cost()

    def get_moves(self):
        return self.moves

    def validate_can_move_to_position(self, position: Point2d):
        if position.x <= 0 or position.x >= self.map.width or position.y <= 0 or position.y >= self.map.height:
            return False

        if position.x == self.position.x and position.y == self.position.y:
            return True

        for obstacle in self.obstacles:
            if obstacle.is_point_inside(position) \
                    or obstacle.does_move_intercourse_obstacle(self.position, position):
                return False
        return True

    def calculate_traveled_distance(self):
        distance = 0.0
        for move_id in range(len(self.moves) - 1):
            pos1 = self.moves[move_id]
            pos2 = self.moves[move_id + 1]
            distance += pos1.count_distance(pos2)
        return round(distance, 3)

    def calculate_distance_from_objective(self):
        return self.position.count_distance(self.objective.position) - self.objective.radius

    def calculate_cost(self):
        self.cost = (self.intersection_moves * 10000 +
                     self.obstacle_proximity * 200 +  # commenting this out keeps uavs closer to the obstacles
                     self.calculate_traveled_distance() +
                     self.calculate_path_smoothness() * 12)

    def get_cost(self):
        if self.cost == 0:
            self.calculate_cost()
        return self.cost

    def calculate_path_smoothness(self):
        angles = []
        for move_id in range(len(self.moves) - 2):
            pos1 = self.moves[move_id]
            pos2 = self.moves[move_id + 1]
            pos3 = self.moves[move_id + 2]
            angle = Point2d.calculate_angle(pos1, pos2, pos3)
            angles.append(angle)
        return max(angles) if angles else 0

    def calculate_obstacle_proximity(self):
        min_distance = min(obstacle.distance_to_point(self.position) for obstacle in self.obstacles)
        self.obstacle_proximity += math.exp(-0.2 * min_distance)
