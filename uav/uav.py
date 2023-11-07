from math import sin, cos, radians, degrees, atan2, pi
from entities.MapObject import MapObject
from entities.Point2d import Point2d

class Genotype:
    def __init__(self, velocity, maneuverability):
        self.velocity = velocity
        self.maneuverability = maneuverability

class UAV:
    def __init__(self, position: Point2d, velocity: float, max_velocity: float, maneuverability: float, objective: MapObject, obstacles: [MapObject]):
        self.current_position = position
        self.moves = [position]
        self.velocity = velocity
        self.max_velocity = max_velocity
        self.maneuverability = maneuverability
        self.objective = objective
        self.obstacles = obstacles
        self.angle = self.stabilize_angle()

    def move_to_position(self, position: Point2d):
        self.moves.append(position)
        self.current_position = position

    def move(self):
        new_position = self.calculate_new_position()

        while self.validate_can_move_to_position(new_position):
            #todo try turning left and right until can move
            new_position = self.calculate_new_position()

        self.current_position = new_position
        self.moves.append(new_position)

    def calculate_new_position(self):
        new_x = self.current_position.x + self.velocity * cos(radians(self.angle))
        new_y = self.current_position.y + self.velocity * sin(radians(self.angle))
        return Point2d(new_x, new_y)

    def stabilize_angle(self):
        dx = self.objective.position.x - self.current_position.x
        dy = self.objective.position.y - self.current_position.y

        initial_angle = degrees(atan2(dy, dx))
        return 360 - (initial_angle + 360) % 360

    def turn(self, direction):
        if direction == "left":
            self.angle -= self.velocity * self.maneuverability
        elif direction == "right":
            self.angle += self.velocity * self.maneuverability

        self.angle %= 360

    def get_moves(self):
        return self.moves

    def set_velocity(self, v: float):
        if v <= self.max_velocity:
            self.velocity = v

    def calculate_traveled_distance(self):
        distance = 0.0
        for move_id in range(len(self.moves) - 1):
            pos1 = self.moves[move_id]
            pos2 = self.moves[move_id + 1]
            distance += pos1.count_distance(pos2)
        return round(distance, 3)

    def validate_can_move_to_position(self, desired_position: Point2d):
        for obstacle in self.obstacles:
            if obstacle.is_point_inside(desired_position)\
                    or obstacle.does_move_intercourse_obstacle(self.current_position, desired_position):
                return False
        return True
