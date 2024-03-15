import random

from map.map import Map
from map.map_object import MapObject
from utils.Point2d import Point2d


class Genotype:
    def __init__(self, position_genes: [Point2d], start_position: Point2d, subobjectives: [Point2d]):
        self.position_genes = position_genes
        self.start_position = start_position
        self.subobjectives = subobjectives

    @classmethod
    def generate_random(cls, num_moves: int, max_x: int, max_y: int, subobjectives: list[Point2d]):
        position_genes = [Point2d(random.randint(0, max_x), random.randint(0, max_y)) for _ in range(num_moves)]
        return cls(position_genes, Point2d(0, 0), subobjectives)

    @classmethod
    def generate_random_with_sorted_by_distance(cls, num_moves: int, start: Point2d, finish: Point2d, subobjectives: list[MapObject]):
        position_genes = [Point2d(random.randint(0, int(finish.x)), random.randint(0, int(finish.y))) for _ in range(num_moves - len(subobjectives))]
        subobjectives_points = []
        for subobjective in subobjectives:
            subobjectives_points.append(subobjective.position)
            position_genes += [subobjective.position]
        position_genes.sort(key=lambda point: start.count_distance(point))
        return cls(position_genes, start, subobjectives_points)

    @classmethod
    def generate_straight(cls, num_moves: int, start: Point2d, finish: Point2d, subobjectives: list[Point2d]):
        step_x = (finish.x - start.x) / num_moves
        step_y = (finish.y - start.y) / num_moves

        # Generate position genes for the straight line (excluding start and finish points)
        position_genes = [Point2d(start.x + i * step_x, start.y + i * step_y) for i in range(1, num_moves)]

        return cls(position_genes, start, subobjectives)

    def mutate(self, map: Map):
        # consider mutating smaller number of genes
        mutate_num = random.randint(0, len(self.position_genes) - 1)
        mutate_index = [random.randint(0, len(self.position_genes) - 1) for _ in range(mutate_num)]
        for index in mutate_index:
            new_position = None
            while new_position is None:
                new_position = Point2d(random.randint(0, map.width), random.randint(0, map.height))
                for obstacle in map.obstacles:
                    if obstacle.is_point_inside(new_position):
                        new_position = None
                        break
            self.position_genes[index] = new_position

    def crossover(self, other):
        filtered_genes1 = self.filter_subobjectives(self.position_genes, self.subobjectives)
        filtered_genes2 = self.filter_subobjectives(other.position_genes, self.subobjectives)

        crossover_point1 = random.randint(0, len(filtered_genes1) - 1)
        crossover_point2 = random.randint(crossover_point1 + 1, len(filtered_genes1))

        preserved_segment = filtered_genes1[crossover_point1:crossover_point2]
        preserved_segment_other = filtered_genes2[crossover_point1:crossover_point2]

        averaged_segment = [Point2d((i.x + j.x) / 2, (i.y + j.y) / 2) for i, j in zip(preserved_segment, preserved_segment_other)]

        offspring_genes = (
            filtered_genes2[:crossover_point1]
            + averaged_segment
            + filtered_genes2[crossover_point2:]
        )

        # offspring_genes = (
        #     other.position_genes[:crossover_point1]
        #     + self.position_genes[crossover_point1:crossover_point2]
        #     + other.position_genes[crossover_point2:]
        # )
        return offspring_genes

    def sort_by_distance(self):
        self.position_genes = sorted(self.position_genes, key=lambda point: self.start_position.count_distance(point))

    @staticmethod
    def filter_subobjectives(genes: [Point2d], subjectives: [Point2d]):
        return list(filter(lambda point: point not in subjectives, genes))

    def add_subjectives(self):
        self.position_genes += self.subobjectives
