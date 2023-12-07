import random
from utils.Point2d import Point2d


class Genotype:
    def __init__(self, position_genes: [Point2d]):
        self.position_genes = position_genes

    @classmethod
    def generate_random(cls, num_moves: int, max_x: int, max_y: int):
        position_genes = [Point2d(random.randint(0, max_x), random.randint(0, max_y)) for _ in range(num_moves)]
        return cls(position_genes)

    @classmethod
    def generate_random_with_sorted_by_distance(cls, num_moves: int, start: Point2d, finish: Point2d):
        position_genes = [Point2d(random.randint(start.x, finish.x), random.randint(start.y, finish.y)) for _ in range(num_moves)]
        position_genes.sort(key=lambda point: start.count_distance(point))
        return cls(position_genes)

    @classmethod
    def generate_straight(cls, num_moves: int, start: Point2d, finish: Point2d):
        step_x = (finish.x - start.x) / num_moves
        step_y = (finish.y - start.y) / num_moves

        # Generate position genes for the straight line (excluding start and finish points)
        position_genes = [Point2d(start.x + i * step_x, start.y + i * step_y) for i in range(1, num_moves)]

        return cls(position_genes)
