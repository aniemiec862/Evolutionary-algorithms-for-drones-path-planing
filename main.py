from uav.uav import UAV, Position
from map.map import Map, MapObjectType, MapObject

if __name__ == "__main__":
    uav = UAV(Position(30, 30), 3, 5, 305, 0.2)
    uav.move_to_position(Position(100, 100))
    uav.move_to_position(Position(300, 180))
    uav.move_to_position(Position(380, 350))
    uav.move_to_position(Position(300, 470))
    uav.move_to_position(Position(400, 800))
    uav.move_to_position(Position(680, 750))
    uav.move_to_position(Position(910, 920))

    uav2 = UAV(Position(30, 30), 3, 5, 305, 0.2)
    uav2.move_to_position(Position(200, 50))
    uav2.move_to_position(Position(400, 80))
    uav2.move_to_position(Position(580, 210))
    uav2.move_to_position(Position(750, 380))
    uav2.move_to_position(Position(870, 590))
    uav2.move_to_position(Position(900, 650))

    points = [
        MapObject(570, 400, 100, MapObjectType.OBSTACLE),
        MapObject(840, 200, 60, MapObjectType.OBSTACLE),
        MapObject(400, 150, 50, MapObjectType.OBSTACLE),
        MapObject(180, 360, 120, MapObjectType.OBSTACLE),
        MapObject(200, 800, 150, MapObjectType.OBSTACLE),
        MapObject(500, 550, 80, MapObjectType.OBSTACLE),
        MapObject(850, 700, 70, MapObjectType.OBSTACLE),
        MapObject(50, 50, 50, MapObjectType.START),
        MapObject(950, 950, 50, MapObjectType.OBJECTIVE)
    ]

    my_map = Map(1000, 1000, points)
    my_map.visualize([uav, uav2])
