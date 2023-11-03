from math import sqrt, sin, cos, radians

class Position:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class Genotype:
    def __init__(self, velocity, maneuverability):
        self.velocity = velocity
        self.maneuverability = maneuverability

class UAV:
    def __init__(self, position: Position, velocity: float, max_velocity: float, angle: float, maneuverability: float):
        self.current_position = position
        self.moves = [position]
        self.velocity = velocity
        self.max_velocity = max_velocity
        self.angle = angle
        self.maneuverability = maneuverability

    def move_to_position(self, position: Position):
        self.moves.append(position)
        self.current_position = position

    def move(self):
        new_x = self.current_position.x + self.velocity * cos(radians(self.angle))
        new_y = self.current_position.y + self.velocity * sin(radians(self.angle))
        new_position = Position(new_x, new_y)

        self.current_position = new_position
        self.moves.append(new_position)

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
            distance += sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)
        return round(distance, 3)
