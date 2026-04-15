import pygame

from src.game.battle import Battle, BattleState, Turn
from src.ui.components import BattleLog, SpellMenu
from src.ui import THEME
from src.ui.panel import Panel
from src.game import State

class BattleScreen:
    def __init__(self, screen, config, sfx, main_menu_button):
        self.screen = screen
        self.config = config
        self.sfx = sfx
        self.back_button = main_menu_button

        self.players = config.create_players()
        self.battle = Battle(self.players[0], self.players[1], self.sfx)
        self.monster_image_cache = {}
        self.battle_log = BattleLog(self.battle)
        self.enemy_action_delay = config.enemy_action_delay

        self.spell_menu = SpellMenu()
        self.show_spell_menu = False
        self.selected_spell_index = None
        self.active_spell_monster = None

        self.background = config.load_random_background(self.screen.get_size())

        self.wave_count = 1
        self.card_rects = []

    def get_attacking_monster(self) -> bool:
        """Returns true if monster is attacking"""
        return self.show_spell_menu

    def update(self):
        self.battle.update()

        if self.battle.state != BattleState.BATTLE_OVER:
            self.battle.battle_is_over()


    def start_new_wave(self):
        self.wave_count += 1
        enemy_team = self.config.create_enemy_team()
        self.players[1] = enemy_team
        self.battle = Battle(self.players[0], self.players[1], self.sfx)
        self.battle_log = BattleLog(self.battle)
        self.close_spell_menu()
        self.background = self.config.load_random_background(self.screen.get_size())  # Regenerate BG

    def reset_battle(self):
        self.players = self.config.create_players()
        self.battle = Battle(self.players[0], self.players[1], self.sfx)
        self.battle_log = BattleLog(self.battle)
        self.close_spell_menu()
        self.card_rects = []

    def get_monster_image(self, image_path: str) -> pygame.Surface:
        """

        :param image_path:
        :return:
        """
        if image_path not in self.monster_image_cache:
            image = pygame.image.load(image_path).convert_alpha()
            cropped_rect = image.get_bounding_rect()
            image = image.subsurface(cropped_rect).copy()
            image = pygame.transform.smoothscale(image, (80, 90))
            self.monster_image_cache[image_path] = image

        return self.monster_image_cache[image_path]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.handle_mouse_click(event.pos)
        return None

    def handle_mouse_click(self, pos: tuple[int, int]) -> State | None:
        if self.back_button.is_hovered(pos):
            return 'menu'

        if self.battle.state == BattleState.ENEMY_TURN:
            return None

        if self.handle_spell_check(pos):
            return None

        if self.battle.state == BattleState.BATTLE_OVER:
            if self.battle.winner == 0:
                self.start_new_wave()
            else:
                self.reset_battle()
            return 'menu'

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

        # Click away from monster to deselect
        if not clicked_monster:
            self.battle.cancel_selection()
            self.close_spell_menu()
            return None
        return None

    def handle_spell_check(self, pos) -> bool:
        if not (self.show_spell_menu and self.active_spell_monster):
            return False

        spell_index = self.spell_menu.get_spell_by_pos(
            self.screen, self.active_spell_monster, pos
        )
        if spell_index is None:
            return False

        self.battle.selected_spell = self.active_spell_monster.known_spells[spell_index]
        self.selected_spell_index = spell_index
        return True

    def get_active_spell(self):
        return self.battle.selected_spell

    def get_active_spell_monster(self):
        return self.active_spell_monster

    def close_spell_menu(self):
        self.show_spell_menu = False
        self.active_spell_monster = None
        self.selected_spell_index = None

    def display_selections(self):
        if self.battle.selected_monster is not None:
            display_text = f' Selected: {self.battle.selected_monster.name}'

            if self.battle.selected_spell is not None:
                display_text += f' | {self.battle.selected_spell.name}'

            info_font = pygame.font.SysFont('Arial', 24)
            display_text_surface = info_font.render(display_text, True, THEME['text_primary'])
            self.screen.blit(display_text_surface, (360, 28))

    def draw_battle_result(self):
        title = ['Draw', 'You Win', 'You Lose'][self.battle.winner or 0]

        # msg = (
        #     f'Wave {self.wave_count} Clear! Click anywhere to start the next wave'
        #     if self.mode == GameMode.WAVE_MODE and self.battle.winner == 0
        #     else 'Click anywhere to return to the menu'
        # )

        msg = f'Round {self.wave_count+1} Click anywhere to continue'

        Panel.draw_popup_message(self.screen, title, msg)

    #TODO: finish this
    def delay_enemy_action(self):
        import time
        time.sleep(70)

    def draw_monster_card(self, monster, card_rect):
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
            energy_text = card_energy_font.render(f'ENG: {monster.energy}/{monster.max_energy}', True,
                                                  THEME['card_stat_text'])
            mp_text = card_energy_font.render(
                f'MP: {monster.mp}/{monster.max_mp}', True, THEME['card_stat_text']
            )

            # display monster's image and hp #TODO: For positioning for stats could do +30 each time in a for loop, also card creation could get a class
            self.screen.blit(name_text, (card_x + 8, card_y + 8))  # Name
            self.screen.blit(monster_img, image_rect)  # Image
            self.screen.blit(hp_text, (card_x + 8, card_y + 130))  # HP
            self.screen.blit(strength_text, (card_x + 8, card_y + 150))  # STR
            self.screen.blit(energy_text, (card_x + 8, card_y + 170))  # ENG
            self.screen.blit(mp_text, (card_x + 8, card_y + 190))  # MP

    def print_cards(self) -> list:
        screen_rect = self.screen.get_rect()
        card_rects = []
        space_between_cards = 10
        card_width, card_height = 112, 220

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
                row_rect.y = top_row_y  # enemy
            else:
                row_rect.y = bottom_row_y  # player

            x = row_rect.left

            for monster in alive_monsters:



                #❌
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
                energy_text = card_energy_font.render(f'ENG: {monster.energy}/{monster.max_energy}', True,
                                                      THEME['card_stat_text'])
                mp_text = card_energy_font.render(
                    f'MP: {monster.mp}/{monster.max_mp}', True, THEME['card_stat_text']
                )

                # display monster's image and hp #TODO: For positioning for stats could do +30 each time in a for loop, also card creation could get a class
                self.screen.blit(name_text, (card_x + 8, card_y + 8))  # Name
                self.screen.blit(monster_img, image_rect)  # Image
                self.screen.blit(hp_text, (card_x + 8, card_y + 130))  # HP
                self.screen.blit(strength_text, (card_x + 8, card_y + 150))  # STR
                self.screen.blit(energy_text, (card_x + 8, card_y + 170))  # ENG
                self.screen.blit(mp_text, (card_x + 8, card_y + 190))  # MP

                x += card_width + space_between_cards

        return card_rects

    def draw(self) -> list:
        self.back_button.draw(self.screen)

        turn = self.battle.current_turn

        if turn == Turn.PLAYER:
            turn_name = 'Player'
        else:
            turn_name = 'AI'
            #TODO: try delay here
            print("ai branch")
            self.delay_enemy_action()

        self.display_selections()

        # Player Turn Text
        info_font = pygame.font.SysFont('Arial', 24)
        turn_text = info_font.render(f'Turn: {turn_name}', True, (255, 255, 255))
        self.screen.blit(turn_text, (200, 28))

        self.card_rects = self.print_cards()

        # Battle Log box
        self.battle_log.draw(self.screen)

        if self.show_spell_menu and self.active_spell_monster and self.active_spell_monster.is_alive():
            self.spell_menu.draw(self.screen, self.active_spell_monster, self.selected_spell_index)


        if self.battle.state == BattleState.BATTLE_OVER:
            self.draw_battle_result()


        return self.card_rects

