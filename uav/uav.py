from map.map import Map
from uav.genotype import Genotype
import math
from utils import constants
from utils.Point2d import Point2d
from utils.Point3d import Point3d

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
        self.path_length = 0
        self.path_smoothness = 0
        self.cost = 0
        self.optimal_height_deviation = 0
        self.vertical_moves_length = 0
        self.avg_height = 0
        self.used_fuel = 0
        self.has_already_moved = False

    def move(self):
        if self.has_already_moved is True:
            return

        self.moves = [self.start.position] + self.genotype.position_genes + [self.objective.position]

        height_sum = 0

        for move_id in range(1, len(self.moves)):
            new_position = self.moves[move_id]
            self.path_length += round(self.position.count_distance(new_position), 3)
            self.optimal_height_deviation += abs(new_position.z - constants.height_to_maintain)
            self.vertical_moves_length += abs(self.position.z - new_position.z)
            height_sum += new_position.z
            if not self.validate_can_move_to_position(new_position):
                self.intersection_moves += 1
            self.calculate_obstacle_proximity()
            self.position = new_position

        self.avg_height = height_sum / (len(self.moves) - 1)
        self.used_fuel = (self.path_length + height_sum * 3) * constants.fuel_consumption

        self.calculate_path_smoothness()
        self.calculate_cost()
        self.has_already_moved = True

    def get_moves(self):
        return self.moves

    def validate_can_move_to_position(self, position: Point3d):
        if Point3d.is_position_between_valid_range(position) is False:
            return False

        # TODO check if we want to move only in z axis
        if position.x == self.position.x and position.y == self.position.y:
            return True

        for obstacle in self.obstacles:
            if obstacle.is_point_inside(position) \
                    or obstacle.does_move_intercourse_obstacle(self.position, position):
                return False

        for uav in constants.final_uavs:
            for point in uav.genotype.position_genes:
                if point is not self.start and point is not self.objective and point not in uav.genotype.subobjectives and position.count_distance(point) < constants.uavs_collision_range:
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
                     self.path_length +
                     self.path_smoothness * 12)

    def get_cost(self):
        if self.path_length == 0:
            self.move()
        if self.cost == 0:
            self.calculate_cost()
        return self.cost

    def calculate_path_smoothness(self):
        angles = []
        for move_id in range(len(self.moves) - 2):
            pos1 = self.moves[move_id]
            pos2 = self.moves[move_id + 1]
            pos3 = self.moves[move_id + 2]
            #TODO calculate in 3d
            angle = Point2d.calculate_angle(pos1, pos2, pos3)
            angles.append(angle)
        self.path_smoothness = sum(map(lambda angle: 180 - angle, angles)) if angles else 0

    def calculate_obstacle_proximity(self):
        min_distance = min(obstacle.distance_to_point(self.position) for obstacle in self.obstacles)
        self.obstacle_proximity += math.exp(-0.2 * min_distance)
