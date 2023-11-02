from map.map import *

if __name__ == "__main__":
    points = [
        Point(57, 40, 10, MapPointType.OBSTACLE),
        Point(84, 20, 6, MapPointType.OBSTACLE),
        Point(40, 15, 5, MapPointType.OBSTACLE),
        Point(18, 36, 12, MapPointType.OBSTACLE),
        Point(20, 80, 15, MapPointType.OBSTACLE),
        Point(50, 55, 8, MapPointType.OBSTACLE),
        Point(85, 70, 7, MapPointType.OBSTACLE),
        Point(5, 5, 5, MapPointType.START),
        Point(95, 95, 5, MapPointType.END)
    ]

    my_map = Map(100, 100, points)
    my_map.visualize()
