import matplotlib.pyplot as plt
import pygame
from matplotlib.backends.backend_agg import FigureCanvasAgg

from map.map_object import MapObject, MapObjectType, MapUAV


class Map:
    def __init__(self, width: int, height: int, start: MapObject, objective: MapObject, obstacles: list[MapObject]):
        self.width = width
        self.height = height

        self.start = start
        self.objective = objective
        self.obstacles = obstacles
        self.points = obstacles + [start, objective]

    def build_plot(self, alg_name, generation_id, uavs):
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
            x, y = point.position.x, point.position.y
            circle = plt.Circle((x, y), point.radius, color=color, fill=True, alpha=0.8)
            ax.add_artist(circle)

        for uav in uavs:
            moves = uav.moves
            if moves:
                x, y = zip(*[(move.x, move.y) for move in moves])
                ax.plot(x, y, marker='o', linestyle='-', markersize=5, linewidth=3.0,
                        label='UAV Path', color=color_mapping[MapObjectType.UAV])
                ax.text(x[-1], y[-1], f"Traveled: {int(uav.distance)}m", fontsize=10, color='black', ha='left',
                        va='bottom')

        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)

        ax.grid(True, which='both', linestyle='--', linewidth=1.0)
        ax.set_title(f'{alg_name}: generation {generation_id}')

        return plt

    def visualize(self, alg_name, generation_id: int, uavs: list[MapUAV]):
        plt = self.build_plot(alg_name, generation_id, uavs)
        plt.show()

    def save_to_image(self, alg_name, generation_id: int, uavs: list[MapUAV]):
        plt = self.build_plot(alg_name, generation_id, uavs)
        canvas = FigureCanvasAgg(plt.figure())
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()
        plt.close()
        return pygame.image.fromstring(raw_data, size, "RGB")
