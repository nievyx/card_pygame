import pygame
from src.ui.theme import THEME

class Panel:
    def __init__(self, width, height, top=None, right_padding=None):
        self.width = width
        self.height = height
        self.top = top
        self.right_padding = right_padding

    def get_rect(self, screen):
        screen_rect = screen.get_rect()
        rect = pygame.Rect(0, 0, self.width, self.height)

        if self.top is not None and self.right_padding is not None:
            rect.topright = (screen_rect.right - self.right_padding, self.top)
        else:
            rect.center = screen_rect.center

        return rect

    def draw_panel(self, screen, title):
        rect = self.get_rect(screen)

        pygame.draw.rect(screen, THEME['battle_log_bg'], rect)
        pygame.draw.rect(screen, THEME['battle_log_border'], rect, 2)

        font = pygame.font.SysFont('Arial', 18)
        title_surface = font.render(title, True, THEME['battle_log_default_text'])
        title_rect = title_surface.get_rect(midtop=(rect.centerx, rect.top + 8))
        screen.blit(title_surface, title_rect)

        return rect

