from entities.MapObject import MapObjectType, MapObject
from entities.Point2d import Point2d
from evolution.Engine import Engine
from map.map import Map

if __name__ == "__main__":
    start = MapObject(Point2d(5, 5), 1, MapObjectType.START)
    objective = MapObject(Point2d(18, 18), 2, MapObjectType.OBJECTIVE)

    obstacles = [
        MapObject(Point2d(10, 10), 3, MapObjectType.OBSTACLE),
    ]

    map = Map(20, 20, start, objective, obstacles)

    no_uavs = 5
    no_iterations = 3
    engine = Engine(no_uavs, no_iterations, map, 5)

    engine.run()

    points = obstacles + [start, objective]

    map.visualize(engine.uavs)
