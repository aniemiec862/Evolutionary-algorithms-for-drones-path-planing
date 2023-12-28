from evolution.evolution_engine import EvolutionEngine
from evolution.objective import OptimizationObjective
from genetic_algorithm.nsga3 import NSGA3
from genetic_algorithm.spea2 import SPEA2
from gui.gui_engine import GUIEngine
from map.map import Map
from map.map_object import MapObject, MapObjectType
from utils.Point2d import Point2d

if __name__ == "__main__":
    start = MapObject(Point2d(5, 5), 1, MapObjectType.START)
    objective = MapObject(Point2d(18, 18), 2, MapObjectType.OBJECTIVE)

    obstacles = [
        MapObject(Point2d(16, 12), 4, MapObjectType.OBSTACLE),
        MapObject(Point2d(7, 9), 2, MapObjectType.OBSTACLE),
        MapObject(Point2d(10, 18), 3, MapObjectType.OBSTACLE),
        MapObject(Point2d(12, 6), 3, MapObjectType.OBSTACLE),
    ]

    map = Map(20, 20, start, objective, obstacles)

    no_uavs = 50
    no_generations = 100
    max_moves_length = 5
    visualize_all_steps = True
    objectives = [OptimizationObjective.PATH_SCORE]
    evolution = EvolutionEngine(no_uavs, no_generations, map, max_moves_length, visualize_all_steps)

    # nsga3 = NSGA3(objectives, 1, 0.1 / no_uavs,  Point2d(map.width, map.height))
    spea2 = SPEA2(objectives, 1, 0.2, Point2d(map.width, map.height), evolution.uavs, 10)

    evolution.run(spea2)

    # gui = GUIEngine(map)
    # gui.run()
