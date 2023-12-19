import pygame

from map.map import Map


class MapCanvas:
    def __init__(self, map: Map):
        self.plot = None
        self.map = map
        self.prepare_plot(0, [])

    def draw(self, screen):
        screen.blit(self.plot, (0, 0))

    def update(self, generation_id, uavs):
        self.prepare_plot(generation_id, uavs)

    def prepare_plot(self, generation_id, uavs):
        self.plot = self.map.save_to_image(generation_id, uavs)
