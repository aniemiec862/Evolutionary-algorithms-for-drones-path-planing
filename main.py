from evolution.evolution_engine import EvolutionEngine
from evolution.objective import OptimizationObjective
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
        # MapObject(Point2d(25, 60), 30, MapObjectType.OBSTACLE),
        MapObject(Point2d(160, 120), 40, MapObjectType.OBSTACLE),
        MapObject(Point2d(80, 90), 30, MapObjectType.OBSTACLE),
        MapObject(Point2d(100, 180), 30, MapObjectType.OBSTACLE),
        MapObject(Point2d(120, 60), 30, MapObjectType.OBSTACLE),
    ]

    map = Map(200, 200, start, objective, obstacles)

    no_uavs = 100
    no_generations = 200
    max_moves_length = 10
    visualize_all_steps = False
    objectives = [OptimizationObjective.PATH_SCORE]
    evolution = EvolutionEngine(no_uavs, no_generations, map, max_moves_length, visualize_all_steps)

    # nsga3 = NSGA3(objectives, 1, 0.1, map)
    spea2 = SPEA2(objectives, 1, 0.1, map, evolution.uavs, int(0.3*no_uavs))

    # evolution.run(nsga3)
    evolution.run(spea2)

    # gui = GUIEngine(map)
    # gui.run()
