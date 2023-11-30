from evolution.engine import Engine
from map.map_object import MapObjectType, MapObject, MapUAV
from utils.Point2d import Point2d

from map.map import Map

if __name__ == "__main__":
    start = MapObject(Point2d(5, 5), 1, MapObjectType.START)
    objective = MapObject(Point2d(18, 18), 2, MapObjectType.OBJECTIVE)

    obstacles = [
        MapObject(Point2d(10, 10), 3, MapObjectType.OBSTACLE),
    ]

    map = Map(20, 20, start, objective, obstacles)

    no_uavs = 200
    no_generations = 200
    max_moves_length = 200
    visualize_all_steps = False
    engine = Engine(no_uavs, no_generations, map, max_moves_length, visualize_all_steps)

    engine.run()
