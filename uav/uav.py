from math import sqrt

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class UAV:
    def __init__(self, position: Position):
        self.current_position = position
        self.moves = [position]

    def move(self, position: Position):
        self.moves.append(position)
        self.current_position = position

    def get_moves(self):
        return self.moves

    def calculate_traveled_distance(self):
        distance = 0.0
        for move_id in range(len(self.moves) - 1):
            pos1 = self.moves[move_id]
            pos2 = self.moves[move_id + 1]
            distance += sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)
        return round(distance, 3)
