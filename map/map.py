import matplotlib.pyplot as plt
import pygame
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg

from map.map_object import MapObject, MapObjectType, MapUAV
from utils import constants


class Map:
    def __init__(self, width: int, depth: int, height: int, start: MapObject, objective: MapObject, obstacles: list[MapObject], subobjectives: list[MapObject]):
        self.width = width
        self.depth = depth
        self.height = height

        self.start = start
        self.objective = objective
        self.obstacles = obstacles
        self.subobjectives = subobjectives
        self.objects = obstacles + subobjectives + [start, objective]

    @staticmethod
    def data_for_cylinder_along_z(center_x, center_y, height_z, radius):
        z = np.linspace(0, height_z, 50)
        theta = np.linspace(0, 2 * np.pi, 50)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = radius * np.cos(theta_grid) + center_x
        y_grid = radius * np.sin(theta_grid) + center_y
        return x_grid, y_grid, z_grid

    @staticmethod
    def data_for_cylinder_top_base(center_x, center_y, height_z, radius):
        R = np.linspace(0, radius, 50)
        h = height_z
        u = np.linspace(0, 2 * np.pi, 50)

        x = np.outer(R, np.cos(u)) + center_x
        y = np.outer(R, np.sin(u)) + center_y
        z = np.ones_like(x) * h
        return x, y, z

    def build_plot(self, alg_name, generation_id, uavs, use_axis_above):
        color_mapping = {
            MapObjectType.START: "green",
            MapObjectType.OBJECTIVE: "blue",
            MapObjectType.OBSTACLE: "red",
            MapObjectType.UAV: "violet",
            MapObjectType.SUBOBJECTIVE: "deepskyblue"
        }

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')

        for object in self.objects:
            color = color_mapping[object.get_type()]
            x, y, z = Map.data_for_cylinder_along_z(object.position.x, object.position.y, object.position.z, object.radius)
            ax.plot_surface(x, y, z, alpha=0.3, color=color)

            x, y, z = Map.data_for_cylinder_top_base(object.position.x, object.position.y, object.position.z, object.radius)
            ax.plot_surface(x, y, z, alpha=0.3, color=color)

        for uav in uavs:
            moves = uav.moves
            if moves:
                x, y, z = zip(*[(move.x, move.y, move.z) for move in moves])
                ax.plot(x, y, z, marker='o', linestyle='-', markersize=5, linewidth=3.0,
                        label='UAV Path', color=color_mapping[MapObjectType.UAV])

        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.depth)
        ax.set_zlim(0, self.height)

        ax.set_xlabel('szerokość [m]', fontsize=14, labelpad=20)
        ax.set_ylabel('głębokość [m]', fontsize=14, labelpad=20)

        if use_axis_above:
            ax.set_zlabel('')
            ax.set_zticks([])
            ax.view_init(elev=90, azim=-90)
        else:
            ax.set_zlabel('wysokość [m]', fontsize=14, labelpad=20)
            ax.view_init(elev=40, azim=-30)

        ax.set_title(f'{alg_name}: generacja {generation_id}, rozmiar populacji {constants.no_uavs}', fontsize=18)
        # additional_parameters = {
        #     "Number of uavs": constants.no_uavs,
        #     "Number of moves": len(uavs[0].moves),
        #     "Path length [m]": uavs[0].distance
        # }

        # vertical_position = 1.05 - len(additional_parameters) * 0.03
        #
        # # Add text for keys (left-aligned)
        # for i, (key, _) in enumerate(additional_parameters.items()):
        #     ax.text2D(0.70, vertical_position - i * 0.03, f"{key}:", transform=ax.transAxes, fontsize=10,
        #               verticalalignment='top', horizontalalignment='left')
        #
        # # Add text for values (right-aligned)
        # for i, (_, value) in enumerate(additional_parameters.items()):
        #     ax.text2D(1.05, vertical_position - i * 0.03, f"{value:>10}", transform=ax.transAxes, fontsize=10,
        #               verticalalignment='top', horizontalalignment='right')

        return plt

    def visualize(self, alg_name, generation_id: int, uavs: list[MapUAV]):
        plt = self.build_plot(alg_name, generation_id, uavs, False)
        plt.show()
        plt = self.build_plot(alg_name, generation_id, uavs, True)
        plt.show()

    def save_to_image(self, alg_name, generation_id: int, uavs: list[MapUAV]):
        plt = self.build_plot(alg_name, generation_id, uavs, False)
        canvas = FigureCanvasAgg(plt.figure())
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()
        plt.close()
        return pygame.image.fromstring(raw_data, size, "RGB")
