from enum import Enum
import matplotlib.pyplot as plt

class MapPointType(Enum):
    START = 1
    END = 2
    OBSTACLE = 3


class Point:
    def __init__(self, x: int, y: int, radius: int, type: MapPointType):
        self.x = x
        self.y = y
        self.radius = radius
        self.type = type

    def set_type(self, new_type: MapPointType):
        self.type = new_type

    def get_type(self):
        return self.type

class Map:
    def __init__(self, width: int, height: int, init_points: list[Point]):
        self.width = width
        self.height = height

        self.points = init_points

    def visualize(self):
        point_colors = {
            MapPointType.START: 'g',
            MapPointType.END: 'b',
            MapPointType.OBSTACLE: 'r'
        }

        plt.figure(figsize=(8, 8))
        ax = plt.gca()

        for point in self.points:
            x, y, point_type = point.x, point.y, point.get_type()
            color = point_colors[point_type]
            circle = plt.Circle((x, y), point.radius, color=color, fill=True)
            ax.add_artist(circle)

        plt.xlim(0, self.width)
        plt.ylim(0, self.height)
        plt.gca().invert_yaxis()  # Invert y-axis to match typical coordinates

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)

        ax.grid(True, which='both', linestyle='--', linewidth=2)

        plt.show()
