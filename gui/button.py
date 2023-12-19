import pygame


class Button:
    def __init__(self, x, y, width, height, text, action, *args, **kwargs):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 128, 255)
        self.text = text
        self.font = pygame.font.Font(None, 20)
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action(*self.args, **self.kwargs)
