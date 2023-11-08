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
        MapObject(Point2d(180, 360), 120, MapObjectType.OBSTACLE),
        MapObject(Point2d(200, 800), 150, MapObjectType.OBSTACLE),
        MapObject(Point2d(500, 550), 80, MapObjectType.OBSTACLE),
        MapObject(Point2d(850, 700), 70, MapObjectType.OBSTACLE)
    ]

    uav = UAV(Point2d(30, 30), 50, 50, 0.2, objective, obstacles)

    while not objective.is_point_inside(uav.current_position):
        uav.move()

    # uav.move_to_position(Point2d(100, 100))
    # uav.move_to_position(Point2d(300, 180))
    # uav.move_to_position(Point2d(380, 350))
    # uav.move_to_position(Point2d(300, 470))
    # uav.move_to_position(Point2d(400, 800))
    # uav.move_to_position(Point2d(680, 750))
    # uav.move_to_position(Point2d(910, 920))
    #
    # uav2 = UAV(Point2d(30, 30), 3, 5, 0.2, objective, obstacles)
    # while not objective.is_point_inside(uav2.current_position):
    #     uav2.move()
    # uav2.move_to_position(Point2d(200, 50))
    # uav2.move_to_position(Point2d(400, 80))
    # uav2.move_to_position(Point2d(580, 210))
    # uav2.move_to_position(Point2d(750, 380))
    # uav2.move_to_position(Point2d(870, 590))
    # uav2.move_to_position(Point2d(900, 650))

    points = obstacles + [start, objective]

    my_map = Map(1000, 1000, points)
    my_map.visualize([uav])
