import pygame

from evolution.evolution_engine import EvolutionEngine
from gui.button import Button
from gui.input_box import InputBox
from map.map import Map
from map.map_object import MapObject, MapObjectType
from utils.Point2d import Point2d


class GUIEngine:
    def __init__(self, no_uavs: int, no_generations: int, max_moves_length: int, visualize_all_steps: bool):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.Font(None, 32)
        pygame.display.set_caption("UAV Simulation")


        input_box1 = InputBox(100, 100, 140, 32)
        input_box2 = InputBox(100, 300, 140, 32)
        self.input_boxes = [input_box1, input_box2]


        start = MapObject(Point2d(5, 5), 1, MapObjectType.START)
        objective = MapObject(Point2d(18, 18), 2, MapObjectType.OBJECTIVE)

        obstacles = [
            MapObject(Point2d(10, 10), 3, MapObjectType.OBSTACLE),
        ]

        map = Map(20, 20, start, objective, obstacles)

        self.evolution_engine = EvolutionEngine(no_uavs, no_generations, map, max_moves_length, visualize_all_steps)

        self.run_button = Button(250, 500, 120, 50, "Run Evolution", self.evolution_engine.run)


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                for box in self.input_boxes:
                    box.handle_event(event)
                self.run_button.handle_event(event)


            for box in self.input_boxes:
                box.update()

            self.screen.fill((30, 30, 30))
            for box in self.input_boxes:
                box.draw(self.screen)
            self.run_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
