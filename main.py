from evolution.evolution_engine import EvolutionEngine
from evolution.objective import OptimizationObjective
from genetic_algorithm.nsga2 import NSGA2
from genetic_algorithm.nsga3 import NSGA3
from genetic_algorithm.spea2 import SPEA2
from map.map import Map
from map.map_object import MapObject, MapObjectType
from utils.Point2d import Point2d

import json

if __name__ == "__main__":
    with open('config.json') as f:
        config = json.load(f)

    start = MapObject(Point2d(config["start"]["x"], config["start"]["y"]), config["start"]["radius"], MapObjectType.START)
    objective = MapObject(Point2d(config["objective"]["x"], config["objective"]["y"]), config["objective"]["radius"], MapObjectType.OBJECTIVE)

    obstacles = [MapObject(Point2d(obstacle["x"], obstacle["y"]), obstacle["radius"], MapObjectType.OBSTACLE) for obstacle in config["obstacles"]]

    subobjectives = [[MapObject(Point2d(subobj["x"], subobj["y"]), subobj["radius"], MapObjectType.SUBOBJECTIVE) for subobj in sublist] for sublist in config["subobjectives"]]

    map = Map(config["width"], config["height"], start, objective, obstacles, [j for i in subobjectives for j in i])

    no_uavs = config["uavs"]
    no_generations = config["generations"]
    max_moves_length = config["moves"]
    visualize_all_steps = config["visualize_all_steps"]

    # objectives = [OptimizationObjective.PATH_SCORE]
    objectives = [OptimizationObjective.OBSTACLE_PROXIMITY,
                  OptimizationObjective.PATH_LENGTH, OptimizationObjective.PATH_SMOOTHNESS]
    evolution = EvolutionEngine(no_uavs, no_generations, map, max_moves_length, visualize_all_steps)

    alg = None
    for subobjects in subobjectives:
        evolution.init_uavs(subobjects)

        if config["algorithm"] == "nsga2":
            alg = NSGA2(objectives, 0.9, 0.05, map, True)
        elif config["algorithm"] == "nsga3":
            alg = NSGA3(objectives, 0.9, 0.05, map, True)
        elif config["algorithm"] == "spea2":
            alg = SPEA2(objectives, 0.9, 0.05, map, evolution.uavs, int(0.3*no_uavs))

        evolution.run(alg)

    evolution.visualize_uavs(alg.get_name(), no_generations, True)
