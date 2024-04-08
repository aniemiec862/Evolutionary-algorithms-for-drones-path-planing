from evolution.evolution_engine import EvolutionEngine
from evolution.objective import OptimizationObjective
from genetic_algorithm.nsga2 import NSGA2
from genetic_algorithm.nsga3 import NSGA3
from genetic_algorithm.spea2 import SPEA2
from map.map import Map
from map.map_object import MapObject, MapObjectType
from utils import constants

import json

from utils.Point3d import Point3d

if __name__ == "__main__":
    with open('config.json') as f:
        config = json.load(f)

    start = MapObject(Point3d(config["start"]["x"], config["start"]["y"], config["start"]["z"]), config["start"]["radius"], MapObjectType.START)
    objective = MapObject(Point3d(config["objective"]["x"], config["objective"]["y"], config["objective"]["z"]), config["objective"]["radius"], MapObjectType.OBJECTIVE)

    obstacles = [MapObject(Point3d(obstacle["x"], obstacle["y"], obstacle["z"]), obstacle["radius"], MapObjectType.OBSTACLE) for obstacle in config["obstacles"]]

    subobjectives = [[MapObject(Point3d(subobjective["x"], subobjective["y"], subobjective["z"]), subobjective["radius"], MapObjectType.SUBOBJECTIVE) for subobjective in sublist] for sublist in config["subobjectives"]]

    map = Map(config["max_width"], config["max_depth"], config["max_height"], start, objective, obstacles, [j for i in subobjectives for j in i])

    no_uavs = config["uavs"]
    constants.no_uavs = no_uavs
    no_generations = config["generations"]
    max_moves_length = config["moves"]
    visualize_all_steps = config["visualize_all_steps"]
    constants.uavs_collision_range = config["uavs_collision_range"]
    constants.max_width = config["max_width"]
    constants.max_depth = config["max_depth"]
    constants.max_height = config["max_height"]
    constants.height_to_maintain = config["height_to_maintain"]
    constants.fuel_consumption = config["fuel_consumption_per_meter"]
    mutation_rate = config["mutation_rate"]
    crossover_rate = config["crossover_rate"]

    # objectives = [OptimizationObjective.PATH_SCORE]
    # objectives = [
    #     OptimizationObjective.OBSTACLE_PROXIMITY,
    #     OptimizationObjective.OPTIMAL_FLIGHT_HEIGHT,
    #     OptimizationObjective.FUEL_CONSUMPTION,
    #     OptimizationObjective.PATH_LENGTH,
    #     OptimizationObjective.PATH_SMOOTHNESS,
    #     OptimizationObjective.HEIGHT_DIFFERENCE
    #               ]

    objectives = [OptimizationObjective.OBSTACLE_PROXIMITY, OptimizationObjective.OPTIMAL_HEIGHT_DEVIATION,
                  OptimizationObjective.PATH_LENGTH, OptimizationObjective.PATH_SMOOTHNESS]
    evolution = EvolutionEngine(no_uavs, no_generations, map, max_moves_length, visualize_all_steps)

    alg = None
    for subobjectives_list in subobjectives:
        evolution.init_uavs(subobjectives_list)

        if config["algorithm"] == "nsga2":
            alg = NSGA2(objectives, crossover_rate, mutation_rate, map, True)
        elif config["algorithm"] == "nsga3":
            alg = NSGA3(objectives, crossover_rate, mutation_rate, map, True)
        elif config["algorithm"] == "spea2":
            alg = SPEA2(objectives, crossover_rate, mutation_rate, map, evolution.uavs, int(0.3*no_uavs))

        evolution.run(alg)

    evolution.visualize_uavs(alg.get_name(), no_generations, True)
