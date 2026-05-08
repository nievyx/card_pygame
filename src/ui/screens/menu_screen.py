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

        self.background = pygame.image.load(
            'src/assets/backgrounds/towering_mountain_biome.png'
        ).convert()

        self.background = pygame.transform.scale(
            self.background,
            self.screen.get_size()
        )


    def handle_click(self, pos: tuple[int, int]) -> State:
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

    def draw_title(self):


        screen_width = self.screen.get_width()

        title_font = pygame.font.SysFont(
            'consolas',
            72
        )

        title_text = title_font.render(
            self.config.game_title,
            True,
            THEME['title_color'])
        title_rect = title_text.get_rect(
            center=(screen_width // 2, 250)
        )

        self.screen.blit(title_text, title_rect)

    def draw(self) -> None:

        self.screen.fill(THEME['background'])

        self.screen.blit(self.background, (0, 0))

        self.draw_title()
        self.start_button.draw(self.screen)
        self.how_to_button.draw(self.screen)
        self.quit_button.draw(self.screen)