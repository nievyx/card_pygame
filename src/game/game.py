import pygame
from pygame.mouse import get_cursor

from src.sound.sfx import SFX
from src.ui import Button, Cursor, THEME
from src.game import State, GameMode
from src.ui.screens.how_to_screen import draw_how_to_play
from src.ui.screens.battle_screen import BattleScreen


class Game:
    def __init__(self, config) -> None:
        pygame.init()
        pygame.display.set_caption(config.game_title)

        self.mode = GameMode.WAVE_MODE
        self.config = config
        self.sfx = SFX()

        fullscreen = 1
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Full Screen
        else:
            self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))  # Original res

        self.background = config.load_random_background(self.screen.get_size())
        self.cursor = Cursor()

        self.current_state: State = 'menu'
        self.running = True
        self.card_rects = [ ]

        # Button Creation
        self.start_button = Button((0, 255, 0), 400, 150, 200, 80, "Start")
        self.how_to_button = Button((0, 0, 255), 400, 300, 420, 80, "How To Play")
        self.quit_button = Button((170, 90, 10), 400, 450, 200, 80, "Quit")
        self.back_button = Button((200, 200, 200), 20, 20, 150, 60, "Back")
        self.main_menu_button = Button((200, 200, 200), 20, 20, 150, 60, "Menu")

        self.battle_screen = BattleScreen(screen=self.screen, config=self.config,
                                          sfx=self.sfx, main_menu_button=self.back_button)

    def start(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def update(self) -> None:
        self.cursor.update()
        if self.current_state == 'game':
            self.battle_screen.update()

            self.update_cursor_context()

    def update_cursor_context(self):
        attacking = self.battle_screen.get_attacking_monster()

        if attacking:
            spell = self.battle_screen.get_active_spell()
            if spell:
                self.cursor.use_spell(spell)
            else:
                self.cursor.use_attack()

        else:
            self.cursor.use_default()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.handle_mouse_click(pos)

    def handle_menu_click(self, pos: tuple[int, int]) -> None:
        if self.start_button.is_hovered(pos):
            self.current_state = 'game'
        elif self.how_to_button.is_hovered(pos):
            self.current_state = 'how_to_play'
        elif self.quit_button.is_hovered(pos):
            self.running = False
        return

    def handle_how_to_play_click(self, pos: tuple[int, int]) -> None:
        if self.back_button.is_hovered(pos):
            self.current_state = 'menu'

    def handle_mouse_click(self, pos: tuple[int, int]) -> None:
        if self.current_state == 'menu':
            self.handle_menu_click(pos)
            return

        if self.current_state == 'game':
            result = self.battle_screen.handle_mouse_click(pos)
            if result is not None:
                self.current_state = result
            return

        if self.current_state == 'how_to_play':
            self.handle_how_to_play_click(pos)


    def display_bg(self):
        self.screen.blit(self.background, (0, 0))

    def draw(self):
        self.screen.fill(THEME['background'])
        self.display_bg()

        if self.current_state == 'menu':
            self.draw_menu()
        elif self.current_state == 'game':
            self.card_rects = self.battle_screen.draw()
        elif self.current_state == 'how_to_play':
            draw_how_to_play(self.screen, self.back_button)

        self.cursor.draw(self.screen)

    def draw_menu(self) -> None:
        self.screen.fill(THEME['background'])
        self.start_button.draw(self.screen)
        self.how_to_button.draw(self.screen)
        self.quit_button.draw(self.screen)

