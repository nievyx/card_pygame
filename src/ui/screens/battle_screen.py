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

        self.enemy_turn_started_at = None
        self.enemy_action_delay = 5.5

        self.background = config.load_random_background(self.screen.get_size())

        self.wave_count = 1
        self.card_rects = []

        self.card_renderer = CardRenderer(battle=self.battle, players=self.players,screen=self.screen)

    def get_attacking_monster(self) -> bool:
        """Returns true if monster is attacking"""
        return self.show_spell_menu

    def delay_enemy_action(self):
        start_ticks = pygame.time.get_ticks()

        if self.enemy_turn_started_at is None:
            self.enemy_turn_started_at = start_ticks
        elif start_ticks - self.enemy_turn_started_at >= self.enemy_action_delay:
            self.battle.update()
            self.enemy_turn_started_at = None
        else:
            self.enemy_turn_started_at = None

    def update(self):
        if self.battle.state != BattleState.ENEMY_TURN:
            self.battle.update()
        elif self.battle.state == BattleState.ENEMY_TURN:
           self.delay_enemy_action()

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
                return None
            else:
                self.reset_battle()
                return 'menu'

        clicked_monster = False

        for rect, player, monster in self.card_rects:
            if not rect.collidepoint(pos):
                continue

            clicked_monster = True

            if player == self.battle.get_current_player():
                if self.battle.try_cast_on_ally(player, monster):
                    self.close_spell_menu()
                else:
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
            self.screen.blit(display_text_surface, (430, 28))

    def draw_battle_result(self):
        if self.battle.winner is None:
            title = None
        elif self.battle.winner == 0:
            title = 'You Win'
        else:
            title = 'You Lose'

        msg = f'Round {self.wave_count+1} Click anywhere to continue'

        Panel.draw_popup_message(self.screen, title, msg)

    def draw(self) -> list:
        self.back_button.draw(self.screen)

        turn = self.battle.current_turn

        if turn == Turn.PLAYER:
            turn_name = 'Player'
        else:
            turn_name = 'AI'

        self.display_selections()

        # Player Turn Text
        info_font = pygame.font.SysFont('Arial', 24)
        wave_text = info_font.render(f'Wave {self.wave_count}', True, THEME['text_primary'])
        turn_text = info_font.render(f'Turn: {turn_name}', True, THEME['text_primary'])
        self.screen.blit(turn_text, (300, 28))
        self.screen.blit(wave_text, (200, 28))

        self.card_rects = self.card_renderer.draw()

        # Battle Log box
        self.battle_log.draw(self.screen)

        if self.show_spell_menu and self.active_spell_monster and self.active_spell_monster.is_alive:
            self.spell_menu.draw(self.screen, self.active_spell_monster, self.selected_spell_index)


        if self.battle.state == BattleState.BATTLE_OVER:
            self.draw_battle_result()


        return self.card_rects

