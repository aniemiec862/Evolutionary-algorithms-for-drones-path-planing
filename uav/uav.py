from utils.Point2d import Point2d
from map.map import Map
from uav.genotype import Genotype


class UAV:
    def __init__(self, genotype: Genotype, map: Map):
        self.genotype = genotype
        self.map = map
        self.start = map.start
        self.objective = map.objective
        self.obstacles = map.obstacles
        self.position = self.start.position
        self.moves = [self.start.position] + genotype.position_genes + [self.objective.position]
        self.is_destroyed = False
        self.has_reach_objective = False
        self.move_counter = 1

    def move(self):
        new_position = self.moves[self.move_counter]
        self.move_counter += 1

        if self.objective.is_point_inside(new_position):
            self.has_reach_objective = True

        if not self.validate_can_move_to_position(new_position):
            self.is_destroyed = True

        self.position = new_position

    def get_moves(self):
        return self.moves

    def validate_can_move_to_position(self, position: Point2d):
        if position.x <= 0 or position.x >= self.map.width or position.y <= 0 or position.y >= self.map.height:
            return False

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
