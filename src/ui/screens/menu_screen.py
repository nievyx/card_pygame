import pygame
from src.ui.theme import THEME
from src.game import State

class MenuScreen:
    def __init__(self, screen, config, start_button, how_to_button, quit_button) -> None:
        self.screen = screen
        self.config = config
        self.start_button = start_button
        self.how_to_button = how_to_button
        self.quit_button = quit_button


    # TODO: add literal
    def handle_click(self, pos: tuple[int, int]):
        if self.start_button.is_hovered(pos):
            return 'game'
        elif self.how_to_button.is_hovered(pos):
            return 'how_to_play'
        elif self.quit_button.is_hovered(pos):
            return 'quit'
        return None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.handle_click(event.pos)
        return None

    def draw(self) -> None:
        self.screen.fill(THEME['background'])
        self.start_button.draw(self.screen)
        self.how_to_button.draw(self.screen)
        self.quit_button.draw(self.screen)