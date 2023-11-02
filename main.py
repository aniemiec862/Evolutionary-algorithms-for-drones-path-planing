from uav.uav import UAV, Position
from map.map import Map, MapObjectType, MapObject

if __name__ == "__main__":
    uav = UAV(Position(3, 3))
    uav.move(Position(10, 10))
    uav.move(Position(30, 18))
    uav.move(Position(38, 35))
    uav.move(Position(30, 47))
    uav.move(Position(40, 80))
    uav.move(Position(68, 75))
    uav.move(Position(95, 95))

    print(uav.calculate_traveled_distance())

    points = [
        MapObject(57, 40, 10, MapObjectType.OBSTACLE),
        MapObject(84, 20, 6, MapObjectType.OBSTACLE),
        MapObject(40, 15, 5, MapObjectType.OBSTACLE),
        MapObject(18, 36, 12, MapObjectType.OBSTACLE),
        MapObject(20, 80, 15, MapObjectType.OBSTACLE),
        MapObject(50, 55, 8, MapObjectType.OBSTACLE),
        MapObject(85, 70, 7, MapObjectType.OBSTACLE),
        MapObject(5, 5, 5, MapObjectType.START),
        MapObject(95, 95, 5, MapObjectType.OBJECTIVE)
    ]

    my_map = Map(100, 100, points)
    my_map.visualize([uav])
