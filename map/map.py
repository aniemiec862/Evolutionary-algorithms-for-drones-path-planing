import matplotlib.pyplot as plt

from map.map_object import MapObject, MapObjectType, MapUAV


class Map:
    def __init__(self, width: int, height: int, start: MapObject, objective: MapObject, obstacles: list[MapObject]):
        self.width = width
        self.height = height

        self.start = start
        self.objective = objective
        self.obstacles = obstacles
        self.points = obstacles + [start, objective]

    def visualize(self, generation_id: int, uavs: list[MapUAV]):
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
            circle = plt.Circle((x, y), point.radius, color=color, fill=True, alpha=0.5)
            ax.add_artist(circle)

        for uav in uavs:
            moves = uav.moves
            if moves:
                x, y = zip(*[(move.x, move.y) for move in moves])
                plt.plot(x, y, marker='o', linestyle='-', markersize=5, linewidth=3.0,
                         label='UAV Path', color=color_mapping[MapObjectType.UAV])
                plt.text(x[-1], y[-1], f"Traveled: {int(uav.distance)}m", fontsize=10, color='black', ha='left', va='bottom')

        plt.xlim(0, self.width)
        plt.ylim(0, self.height)

        plt.grid(True)
        ax.grid(True, which='both', linestyle='--', linewidth=1.0)
        plt.title(f'Generation {generation_id}')

        plt.show()
