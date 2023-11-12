from entities.MapObject import MapObject
from entities.Point2d import Point2d
from uav.genotype import Genotype, MoveGene


class UAV:
    def __init__(self, genotype: Genotype, start: MapObject, objective: MapObject, obstacles: list[MapObject]):
        self.genotype = genotype
        self.start = start
        self.objective = objective
        self.obstacles = obstacles
        self.position = self.start.position
        self.moves = [self.start.position]
        self.is_destroyed = False
        self.has_reach_objective = False
        self.move_counter = 0

    def move_to_position(self, position: Point2d):
        self.moves.append(position)
        self.position = position

    def move(self):
        move_gene = self.genotype.move_genes[self.move_counter]
        self.move_counter += 1

        new_position = self.calculate_new_position(move_gene)

        if self.objective.is_point_inside(new_position):
            self.has_reach_objective = True

        if not self.validate_can_move_to_position(new_position):
            self.is_destroyed = True

        self.position = new_position
        self.moves.append(new_position)

    def calculate_new_position(self, move_gene: MoveGene):
        move_vector = move_gene.to_vector()
        return Point2d(self.position.x + move_vector.x, self.position.y + move_vector.y)

    def get_moves(self):
        return self.moves

    def calculate_traveled_distance(self):
        distance = 0.0
        for move_id in range(len(self.moves) - 1):
            pos1 = self.moves[move_id]
            pos2 = self.moves[move_id + 1]
            distance += pos1.count_distance(pos2)
        return round(distance, 3)

    def validate_can_move_to_position(self, position: Point2d):
        for obstacle in self.obstacles:
            if obstacle.is_point_inside(position) \
                    or obstacle.does_move_intercourse_obstacle(self.position, position):
                return False
        return True

    def reset(self):
        self.move_counter = 0
        self.position = self.start.position
        self.moves = [self.start.position]
