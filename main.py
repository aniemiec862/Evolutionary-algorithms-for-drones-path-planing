from evolution.evolution_engine import EvolutionEngine
from gui.gui_engine import GUIEngine
from map.map import Map
from map.map_object import MapObject, MapObjectType
from utils.Point2d import Point2d

if __name__ == "__main__":
    # start = MapObject(Point2d(5, 5), 1, MapObjectType.START)
    # objective = MapObject(Point2d(18, 18), 2, MapObjectType.OBJECTIVE)
    #
    # obstacles = [
    #     MapObject(Point2d(10, 10), 3, MapObjectType.OBSTACLE),
    # ]
    #
    # map = Map(20, 20, start, objective, obstacles)

    no_uavs = 50
    no_generations = 1000
    max_moves_length = 30
    visualize_all_steps = False
    # evolution = EvolutionEngine(no_uavs, no_generations, map, max_moves_length, visualize_all_steps)
    #
    # evolution.run()

    gui = GUIEngine(no_uavs, no_generations, max_moves_length, visualize_all_steps)
    gui.run()
