import pygame

from src.game.battle import Battle, BattleState, Turn
from src.ui.components import BattleLog, SpellMenu
from src.ui.cards.card_renderer import CardRenderer
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

        self.card_renderer = CardRenderer(battle=self.battle, players=self.players,screen=self.screen)
        # ❌ Temp for card frame (Refactor to CardRenderer)
        self.card_frame = pygame.image.load('src/assets/frame/1.png').convert_alpha()
        self.card_frame = pygame.transform.smoothscale(self.card_frame, (112, 220)) # try 112, 220

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

    # ❌
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
        time.sleep(7)

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

        self.card_rects = self.card_renderer.print_cards()

        # Battle Log box
        self.battle_log.draw(self.screen)

        if self.show_spell_menu and self.active_spell_monster and self.active_spell_monster.is_alive():
            self.spell_menu.draw(self.screen, self.active_spell_monster, self.selected_spell_index)


        if self.battle.state == BattleState.BATTLE_OVER:
            self.draw_battle_result()


        return self.card_rects

