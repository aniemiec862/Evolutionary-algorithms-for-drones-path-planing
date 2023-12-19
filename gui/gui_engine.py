import pygame

from evolution.evolution_engine import EvolutionEngine
from evolution.objective import OptimizationObjective
from genetic_algorithm.nsga3 import NSGA3
from gui.button import Button
from gui.input_box import InputBox
from gui.map_canvas import MapCanvas
from map.map import Map
from utils.Point2d import Point2d


class GUIEngine:
    def __init__(self, map: Map):
        pygame.init()
        self.map = map
        # self.map_canvas = MapCanvas(map)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.Font(None, 32)
        pygame.display.set_caption("UAV Simulation")

        self.no_uavs_input = InputBox(100, 480, 100, 32, 'uavs', '100')
        self.no_generations = InputBox(100, 550, 100, 32, 'generations', '10')
        self.input_boxes = [self.no_uavs_input, self.no_generations]

        self.run_button = Button(450, 500, 120, 50, "Run Evolution", self.run_evolution)


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

            self.screen.fill((30, 30, 30))
            for box in self.input_boxes:
                box.draw(self.screen)
            self.run_button.draw(self.screen)
            # self.map_canvas.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def run_evolution(self):
        no_uavs = int(self.no_uavs_input.text)
        no_generations = int(self.no_generations.text)
        max_moves_length = 15
        visualize_all_steps = False

        nsga3 = NSGA3([OptimizationObjective.PATH_SCORE], 1, 0.1 / no_uavs, Point2d(self.map.width, self.map.height))

        evolution_engine = EvolutionEngine(no_uavs, no_generations, self.map, max_moves_length, visualize_all_steps)
        evolution_engine.run(nsga3)
        # self.map_canvas.update(no_generations, evolution_engine.get_map_uavs())
