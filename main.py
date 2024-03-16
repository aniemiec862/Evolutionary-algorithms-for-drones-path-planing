from evolution.evolution_engine import EvolutionEngine
from evolution.objective import OptimizationObjective
from genetic_algorithm.nsga2 import NSGA2
from genetic_algorithm.nsga3 import NSGA3
from genetic_algorithm.spea2 import SPEA2
from gui.gui_engine import GUIEngine
from map.map import Map
from map.map_object import MapObject, MapObjectType
from utils.Point2d import Point2d

if __name__ == "__main__":
    start = MapObject(Point2d(20, 20), 10, MapObjectType.START)
    objective = MapObject(Point2d(180, 180), 20, MapObjectType.OBJECTIVE)

    obstacles = [
        MapObject(Point2d(100, 180), 30, MapObjectType.OBSTACLE),
        MapObject(Point2d(120, 60), 30, MapObjectType.OBSTACLE),
    ]

    subobjectives = [
        MapObject(Point2d(75, 125), 5, MapObjectType.SUBOBJECTIVE),
        MapObject(Point2d(180, 50), 5, MapObjectType.SUBOBJECTIVE),
    ]

    map = Map(200, 200, start, objective, obstacles, subobjectives)

    no_uavs = 500
    no_generations = 50
    max_moves_length = 5
    visualize_all_steps = False
    # objectives = [OptimizationObjective.PATH_SCORE]
    objectives = [OptimizationObjective.OBSTACLE_PROXIMITY,
                  OptimizationObjective.PATH_LENGTH, OptimizationObjective.PATH_SMOOTHNESS]
    evolution = EvolutionEngine(no_uavs, no_generations, map, max_moves_length, visualize_all_steps)

    alg = None
    for subobject in subobjectives:
        evolution.init_uavs([subobject])

        # alg = NSGA2(objectives, 0.8, 0.05, map, True)
        # alg = NSGA3(objectives, 0.8, 0.05, map, True)
        alg = SPEA2(objectives, 0.8, 0.05, map, evolution.uavs, int(0.3*no_uavs))

        evolution.run(alg)

    evolution.visualize_uavs(alg.get_name(), no_generations, True)

    # gui = GUIEngine(map)
    # gui.run()
