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
