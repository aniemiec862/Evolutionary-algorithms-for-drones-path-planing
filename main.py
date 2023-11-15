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

    no_uavs = 3
    no_generations = 1
    max_moves_length = 50
    engine = Engine(no_uavs, no_generations, map, 50)

    engine.run()

    list_of_map_uavs = [MapUAV(uav.get_moves(), uav.calculate_traveled_distance()) for uav in engine.uavs]
    map.visualize(list_of_map_uavs)
