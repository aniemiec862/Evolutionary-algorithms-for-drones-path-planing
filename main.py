from entities.MapObject import MapObjectType, MapObject
from entities.Point2d import Point2d
from uav.uav import UAV
from map.map import Map

if __name__ == "__main__":
    start = MapObject(Point2d(50, 50), 50, MapObjectType.START)
    objective = MapObject(Point2d(950, 950), 50, MapObjectType.OBJECTIVE)

    obstacles = [
        MapObject(Point2d(500, 500), 100, MapObjectType.OBSTACLE),
        MapObject(Point2d(840, 200), 60, MapObjectType.OBSTACLE),
        MapObject(Point2d(400, 150), 50, MapObjectType.OBSTACLE),
        MapObject(Point2d(180, 320), 120, MapObjectType.OBSTACLE),
        MapObject(Point2d(200, 800), 150, MapObjectType.OBSTACLE),
        MapObject(Point2d(500, 550), 80, MapObjectType.OBSTACLE),
        MapObject(Point2d(800, 700), 70, MapObjectType.OBSTACLE)
    ]

    uav = UAV(Point2d(30, 30), 50, 50, 0.2, objective, obstacles)

    while not objective.is_point_inside(uav.current_position):
        uav.move()

    points = obstacles + [start, objective]

    my_map = Map(1000, 1000, points)
    my_map.visualize([uav])
