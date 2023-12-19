from evolution.evolution_engine import EvolutionEngine
from evolution.objective import OptimizationObjective
from genetic_algorithm.nsga3 import NSGA3
from gui.gui_engine import GUIEngine
from map.map import Map
from map.map_object import MapObject, MapObjectType
from utils.Point2d import Point2d

if __name__ == "__main__":
    start = MapObject(Point2d(5, 5), 1, MapObjectType.START)
    objective = MapObject(Point2d(18, 18), 2, MapObjectType.OBJECTIVE)

    obstacles = [
        MapObject(Point2d(14, 10), 3, MapObjectType.OBSTACLE),
    ]

    map = Map(20, 20, start, objective, obstacles)

    no_uavs = 100
    no_generations = 10
    max_moves_length = 15
    visualize_all_steps = False
    objectives = [OptimizationObjective.PATH_SCORE]
    evolution = EvolutionEngine(no_uavs, no_generations, map, max_moves_length, visualize_all_steps)

    nsga3 = NSGA3(objectives, 1, 0.1 / no_uavs,  Point2d(map.width, map.height))

    # evolution.run(nsga3)

    gui = GUIEngine(map)
    gui.run()
