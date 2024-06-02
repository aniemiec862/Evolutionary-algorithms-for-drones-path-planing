import string
import time

from evolution.objective import OptimizationObjective
from genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from map.map import Map
from map.map_object import MapUAV, MapObject
from uav.genotype import Genotype
from uav.uav import UAV
from utils import constants
from utils.Point3d import Point3d
from utils.Results import Results


class EvolutionEngine:
    def __init__(self, no_uavs: int, no_generations: int, map: Map, max_moves_length: int, visualize_all_steps: bool, objectives: [OptimizationObjective],):
        self.uavs = []
        self.no_uavs = no_uavs
        self.no_generations = no_generations
        self.map = map
        self.max_moves_length = max_moves_length
        self.visualize_all_steps = visualize_all_steps
        self.results = Results(objectives)
        constants.final_uavs = []

    def init_uavs(self, subobjectives: list[MapObject]):
        uavs = []
        for _ in range(self.no_uavs):
            genotype = Genotype.generate_random_with_sorted_by_distance(self.max_moves_length, self.map.start.position, self.map.objective.position, subobjectives)
            uavs.append(UAV(genotype, self.map))
        self.uavs = uavs

    def run(self, algorithm: GeneticAlgorithm):
        start = time.time()
        for gen_id in range(self.no_generations):
            print("Gen: ", gen_id + 1)
            self.run_generation(gen_id, algorithm)

        self.results.alg.append(algorithm.get_name())
        self.results.generations.append(self.no_generations)
        self.results.times.append(time.time() - start)
        self.results.population_size.append(self.no_uavs)
        constants.final_uavs += self.uavs[:constants.final_uavs_per_path]

        # if self.visualize_all_steps is False:
        #     self.visualize_uavs(algorithm.get_name(), self.no_generations, False)

    def run_generation(self, gen_id, algorithm: GeneticAlgorithm):
        for uav in self.uavs:
            uav.move()

        if self.visualize_all_steps is True:
            self.visualize_uavs(algorithm.get_name(), gen_id + 1, False)

        if gen_id + 1 == self.no_generations:
            return

        self.uavs = algorithm.run_generation(self.uavs)

    def create_map_uavs(self, list_of_points: [[(float, float, float)]]):
        uavs = []
        for points in list_of_points:
            point_objects = [Point3d(x, y, z) for x, y, z in points]
            point_objects.insert(0, self.map.start.position)
            point_objects.append(self.map.objective.position)
            uav = MapUAV(point_objects, 0)
            uavs.append(uav)
        return uavs

    def visualize_uavs(self, algorithm_name: string, generation_id: int, is_final_result: bool):
        self.print_uavs()
        if is_final_result:
            uavs = [MapUAV(uav.get_moves(), uav.calculate_traveled_distance()) for uav in constants.final_uavs]
        else:
            uavs = [MapUAV(uav.get_moves(), uav.calculate_traveled_distance()) for uav in self.uavs[:constants.final_uavs_per_path]]

        # p1 = [(4, 1, 8), (3, 5, 17), (10, 10, 20), (25, 25, 50), (36, 38, 66), (35, 42, 5), (40, 40, 75)]
        # p2 = [(3, 9, 6), (1, 25, 2), (8, 17, 28), (5, 20, 35), (1, 26, 48), (10, 45, 50), (30, 45, 75)]
        # p3 = [(10, 5, 5), (18, 6, 12), (20, 5, 25), (47, 2, 22), (45, 10, 50), (45, 30, 75)]
        #
        # all_points = [p1, p2, p3]

        # uavs = self.create_map_uavs(all_points)
        self.map.visualize(algorithm_name, generation_id, uavs)

    def print_uavs(self):
        for uav in constants.final_uavs:
            coordinates = [(point.x, point.y, point.z) for point in uav.genotype.position_genes]
            print(coordinates)

    def save_results(self, file_name: string, objectives: [OptimizationObjective]):
        for uav in constants.final_uavs:
            for count, objective in enumerate(objectives):
                self.results.objectives_values[count].append(GeneticAlgorithm.objective_function(uav, objective))

        self.results.save_to_file(file_name, True)
