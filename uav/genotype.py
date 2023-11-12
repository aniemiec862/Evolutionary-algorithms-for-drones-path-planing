from enum import Enum
from entities.Point2d import Point2d


class MoveGene(Enum):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7

    def to_vector(self):
        if self.value == 0:
            return Point2d(0, 1)
        elif self.value == 1:
            return Point2d(1, 1)
        elif self.value == 2:
            return Point2d(1, 0)
        elif self.value == 3:
            return Point2d(1, -1)
        elif self.value == 4:
            return Point2d(0, -1)
        elif self.value == 5:
            return Point2d(-1, -1)
        elif self.value == 6:
            return Point2d(-1, 0)
        elif self.value == 7:
            return Point2d(-1, 1)


class Genotype:
    def __init__(self, move_genes: [MoveGene]):
        self.move_genes = move_genes

    @classmethod
    def generate_random(cls, num_moves):
        import random
        move_genes = [MoveGene(random.randint(0, 7)) for _ in range(num_moves)]
        return cls(move_genes)
