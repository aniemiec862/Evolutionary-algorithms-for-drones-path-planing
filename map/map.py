from enum import Enum
from uav.uav import UAV
import matplotlib.pyplot as plt


class MapObjectType(Enum):
    START = 0
    OBJECTIVE = 1
    OBSTACLE = 2
    UAV = 3

class MapObject:
    def __init__(self, x: int, y: int, radius: int, type: MapObjectType):
        self.x = x
        self.y = y
        self.radius = radius
        self.type = type

    def set_type(self, new_type: MapObjectType):
        self.type = new_type

    def get_type(self):
        return self.type

class Map:
    def __init__(self, width: int, height: int, init_points: list[MapObject]):
        self.width = width
        self.height = height

        self.points = init_points

    def visualize(self, uavs: list[UAV]):
        color_mapping = {
            MapObjectType.START: "green",
            MapObjectType.OBJECTIVE: "blue",
            MapObjectType.OBSTACLE: "red",
            MapObjectType.UAV: "violet"
        }

        plt.figure(figsize=(8, 8))
        ax = plt.gca()

        for point in self.points:
            color = color_mapping[point.get_type()]
            x, y, point_type = point.x, point.y, point.get_type()
            circle = plt.Circle((x, y), point.radius, color=color, fill=True)
            ax.add_artist(circle)

        for uav in uavs:
            moves = uav.get_moves()
            if moves:
                x, y = zip(*[(move.x, move.y) for move in moves])
                plt.plot(x, y, marker='o', linestyle='-', markersize=5, linewidth=3.0,
                         label='UAV Path', color=color_mapping[MapObjectType.UAV])

        plt.xlim(0, self.width)
        plt.ylim(0, self.height)
        plt.gca().invert_yaxis()

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)

        ax.grid(True, which='both', linestyle='--', linewidth=1.0)

        plt.show()
