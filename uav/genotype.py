import random
from utils.Point2d import Point2d


class Genotype:
    def __init__(self, position_genes: [Point2d]):
        self.position_genes = position_genes

    @classmethod
    def generate_random(cls, num_moves: int, max_x: int, max_y: int):
        position_genes = [Point2d(random.randint(0, max_x), random.randint(0, max_y)) for _ in range(num_moves)]
        return cls(position_genes)
