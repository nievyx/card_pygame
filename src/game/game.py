from enum import Enum, auto

import pygame
from typing import Literal
from src.game.battle import Battle, BattleState, Turn
from src.sound import sfx
from src.ui.components import BattleLog, SpellMenu
from src.sound.sfx import SFX
from src.ui import Button, THEME
from src.ui.panel import Panel

State = Literal['menu', 'game', 'how_to_play', 'quit']

class GameMode(Enum):
    WAVE_MODE = auto()

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
            self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT)) #Orginial res

        self.background = config.load_random_background(self.screen.get_size())

        self.current_state: State = 'menu'
        self.running = True
        self.card_rects = [ ]

        self.players = config.create_players()
        self.battle = Battle(self.players[0], self.players[1], self.sfx)
        self.monster_image_cache = {}
        self.battle_log = BattleLog(self.battle)

        self.spell_menu = SpellMenu()
        self.show_spell_menu = False
        self.selected_spell_index = None
        self.active_spell_monster = None

        # Button Creation
        self.start_button = Button((0, 255, 0), 400, 150, 200, 80, "Start")
        self.how_to_button = Button((0, 0, 255), 400, 300, 420, 80, "How To Play")
        self.quit_button = Button((170, 90, 10), 400, 450, 200, 80, "Quit")
        self.back_button = Button((200, 200, 200), 20, 20, 150, 60, "Back")
        self.main_menu_button = Button((200, 200, 200), 20, 20, 150, 60, "Menu")

        self.wave_count = 1

    def start_new_wave(self):
        self.wave_count += 1
        enemy_team = self.config.create_enemy_team()
        self.players[1] = enemy_team
        self.battle = Battle(self.players[0], self.players[1], self.sfx)
        self.battle_log = BattleLog(self.battle)
        self.close_spell_menu()
        self.background = self.config.load_random_background(self.screen.get_size()) #Regenerate BG

    def reset_battle(self):
        self.players = self.config.create_players()
        self.battle = Battle(self.players[0], self.players[1], self.sfx)
        self.battle_log = BattleLog(self.battle)
        self.close_spell_menu()
        self.card_rects = []

    def get_monster_image(self, image_path: str) -> pygame.Surface:
        if image_path not in self.monster_image_cache:
            image = pygame.image.load(image_path).convert_alpha()
            cropped_rect = image.get_bounding_rect()
            image = image.subsurface(cropped_rect).copy()
            image = pygame.transform.smoothscale(image, (80, 90))
            self.monster_image_cache[image_path] = image

        return self.monster_image_cache[image_path]

    def start(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def update(self) -> None:
        if self.current_state == 'game':
            self.battle.update()

            if self.battle.state != BattleState.BATTLE_OVER:
                self.battle.battle_is_over()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.handle_mouse_click(pos)

    def close_spell_menu(self):
        self.show_spell_menu = False
        self.active_spell_monster = None
        self.selected_spell_index = 0

    def handle_menu_click(self, pos: tuple[int, int]) -> None:
        if self.start_button.is_hovered(pos):
            self.current_state = 'game'
        elif self.how_to_button.is_hovered(pos):
            self.current_state = 'how_to_play'
        elif self.quit_button.is_hovered(pos):
            self.running = False
        return

    def handle_game_click(self, pos: tuple[int, int]) -> None:
        if self.back_button.is_hovered(pos):
            self.current_state = 'menu'
            return

        if self.battle.state == BattleState.ENEMY_TURN:
            return

        if self.battle.state == BattleState.BATTLE_OVER:
            if self.battle.winner == 0:
                self.start_new_wave()
            else:
                self.reset_battle()
            return

        clicked_monster = False

        for rect, player, monster in self.card_rects:
            if not rect.collidepoint(pos):
                continue

            clicked_monster = True

            if player == self.battle.get_current_player():
                self.battle.select_monster(player, monster)

                if monster.known_spells:
                    self.show_spell_menu = True
                    self.active_spell_monster = monster
                else:
                    self.close_spell_menu()

            elif player == self.battle.get_opposing_player():  #
                self.close_spell_menu()
                self.battle.try_attack(player, monster)
            break

        if not clicked_monster:
            # Click away from monster to deselect
            self.battle.cancel_selection()
            self.close_spell_menu()

    def handle_how_to_play_click(self, pos: tuple[int, int]) -> None:
        if self.back_button.is_hovered(pos):
            self.current_state = 'menu'

    def handle_mouse_click(self, pos: tuple[int, int]) -> None:
        if self.current_state == 'menu':
            self.handle_menu_click(pos)
            return
        if self.current_state == 'game':
            self.handle_game_click(pos)
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
            self.card_rects = self.draw_game()
        elif self.current_state == 'how_to_play':
            self.draw_how_to_play()

    def draw_menu(self) -> None:
        self.screen.fill(THEME['background'])
        self.start_button.draw(self.screen)
        self.how_to_button.draw(self.screen)
        self.quit_button.draw(self.screen)

    def draw_how_to_play(self) -> None:
        self.back_button.draw(self.screen)
        # TODO: do u want the game bg

        #TODO: add instructions. And add font to config, move instructions elsewhere as well
        #TODO: should instructions be a txt or a md and then just a quick func to read ir
        font = pygame.font.SysFont('Arial', 40)
        #TODO : Put text in the box, believe it's in panel class
        text = font.render('How to play instructions will go here.....', 1, (0, 0, 0))

        self.screen.blit(text, (200,300))
        #self.screen.blit(text, (self.SCREEN_WIDTH / 2 - text.get_width() / 2, self.SCREEN_HEIGHT / 2 - text.get_height() / 2))

    def display_selections(self):
        if self.battle.selected_monster is not None:
            display_text = f' Selected: {self.battle.selected_monster.name}'

            if self.battle.selected_spell is not None:
                display_text += f' | {self.battle.selected_spell.name}'

            info_font = pygame.font.SysFont('Arial', 24)
            display_text_surface = info_font.render(display_text, True, THEME['text_primary'])
            self.screen.blit(display_text_surface, (360,28))

    def draw_battle_result(self):
        title = ['Draw', 'You Win', 'You Lose'][self.battle.winner or 0]

        msg = (
            f'Wave {self.wave_count} Clear! Click anywhere to start the next wave'
            if self.mode == GameMode.WAVE_MODE and self.battle.winner == 0
            else 'Click anywhere to return to the menu'
        )

        Panel.draw_popup_message(self.screen, title, msg)

    def draw_game(self) -> list:
        self.main_menu_button.draw(self.screen)
        card_rects = []  # For cards rectangle space

        card_width, card_height = 112, 220
        space_between_cards = 10
        initial_x = 20
        initial_y = 80
        y_offset = card_height + 40

        turn = self.battle.current_turn


        if turn == Turn.PLAYER:
            turn_name = 'Player'
        else:
            turn_name = 'AI'


        self.display_selections()

        # Player Turn Text
        info_font = pygame.font.SysFont('Arial', 24)
        turn_text = info_font.render(f'Turn: {turn_name}', True, (255, 255, 255))
        self.screen.blit(turn_text, (200, 28))

        screen_rect = self.screen.get_rect()

        # Print the cards
        for row_index, (player, monsters) in enumerate(self.players.items()):
            alive_monsters = [monster for monster in monsters if monster.is_alive()]
            num_cards = len(alive_monsters)

            total_width = num_cards * card_width + (num_cards - 1) * space_between_cards

            row_rect = pygame.Rect(0, 0, total_width, card_height)
            row_rect.centerx = screen_rect.centerx
            # row_rect.y = initial_y + (row_index * y_offset)

            top_row_y = 80
            bottom_row_y = screen_rect.bottom - card_height - 80

            # Choose which player goes on top / bottom
            if row_index == 1:
                row_rect.y = top_row_y # enemy
            else:
                row_rect.y = bottom_row_y # player

            x = row_rect.left

            for monster in alive_monsters:
                card_x = x
                card_y = row_rect.y

                # create rect for card (used for clicking)
                card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
                card_rects.append((card_rect, player, monster))

                # draw card background
                pygame.draw.rect(self.screen, THEME['card_color'], card_rect)  # COLOR: gray 50, 50, 50

                # Highlight selected card
                if monster == self.battle.selected_monster:
                    pygame.draw.rect(self.screen, THEME['card_selected'], card_rect, 3)  # bright yellow

                # load + scale monster image
                monster_img = self.get_monster_image(monster.image)

                image_rect = monster_img.get_rect()
                image_rect.centerx = card_rect.centerx
                image_rect.top = card_y + 40

                # draw text
                card_name_font = pygame.font.SysFont('Arial', 20, bold=False)
                name_text = card_name_font.render(f'{monster.name}', True, (255, 255, 255))

                def get_stat_color(current, max_value):
                    """Toggles stat colors to highlight low stats"""
                    if max_value <= 0:
                        return THEME['text_secondary']
                    percent = 0.3
                    return THEME['card_stat_low'] if current / max_value <= percent else THEME['text_secondary']

                # TODO: use a stats variable and get it from themes / create it and then move it to themes

                hp_text_font = pygame.font.SysFont('Arial', 16)  # TODO: add font to config
                hp_color = get_stat_color(monster.hp, monster.max_hp)
                hp_text = hp_text_font.render(f'HP: {monster.hp}/{monster.max_hp}', True, hp_color)

                card_strength_font = pygame.font.SysFont('Arial', 16, bold=False)
                strength_text = card_strength_font.render(f'STR: {monster.strength}', True, THEME['card_stat_text'])

                card_energy_font = pygame.font.SysFont('Arial', 16, bold=False)
                energy_text = card_energy_font.render(f'ENG: {monster.energy}/{monster.max_energy}', True, THEME['card_stat_text'])

                # display monster's image and hp #TODO: For positioning for stats could do +30 each time in a for loop, also card creation could get a class
                self.screen.blit(name_text, (card_x + 8, card_y + 8))  # Name
                self.screen.blit(monster_img, image_rect)  # Image
                self.screen.blit(hp_text, (card_x + 8, card_y + 130))  # HP
                self.screen.blit(strength_text, (card_x + 8, card_y + 150))  # STR
                self.screen.blit(energy_text, (card_x + 8, card_y + 170))  # ENG

                x += card_width + space_between_cards

            self.battle_log.draw(self.screen) # Battle Log box

            if self.show_spell_menu and self.active_spell_monster and self.active_spell_monster.is_alive():
                self.spell_menu.draw(self.screen, self.active_spell_monster, self.selected_spell_index)


            if self.battle.state == BattleState.BATTLE_OVER:
                self.draw_battle_result()




        return card_rects






