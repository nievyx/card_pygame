import pygame
from typing import Literal
from src.game.battle.battle import Battle, BattleState, Turn #TODO: also make import cleaner via __init__.py
from src.ui.components.battle_log import BattleLog
from src.ui import Button

State = Literal['menu', 'game', 'how_to_play', 'quit']

class Game:
    def __init__(self, config) -> None:
        pygame.init()
        self.config = config
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.game_title)

        self.current_state: State = 'menu'
        self.running = True
        self.card_rects = [ ]

        self.players = config.create_players()
        self.battle = Battle(self.players[0], self.players[1])
        self.monster_image_cache = {}
        self.battle_log = BattleLog(self.battle)

        # Button Creation
        self.start_button = Button((0, 255, 0), 400, 150, 200, 80, "Start")
        self.how_to_button = Button((0, 0, 255), 400, 300, 420, 80, "How To Play")
        self.quit_button = Button((170, 90, 10), 400, 450, 200, 80, "Quit")
        self.back_button = Button((200, 200, 200), 20, 20, 150, 60, "Back")
        self.main_menu_button = Button((200, 200, 200), 20, 20, 150, 60, "Menu")

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

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.handle_mouse_click(pos)

    def handle_mouse_click(self, pos: tuple[int, int]) -> None:
        if self.current_state == 'menu':
            if self.start_button.is_hovered(pos):
                self.current_state = 'game'

            elif self.how_to_button.is_hovered(pos):
                self.current_state = 'how_to_play'

            elif self.quit_button.is_hovered(pos):
                self.running = False #TODO: should handle_mouse clicks control this logic

        elif self.current_state == 'game':
            if self.back_button.is_hovered(pos):
                self.current_state = 'menu'
                return

            if self.battle.state == BattleState.ENEMY_TURN:
                return

            if self.battle.state == BattleState.BATTLE_OVER:
                return

            for rect, player, monster in self.card_rects:
                if not rect.collidepoint(pos):
                    continue

                if player == self.battle.get_current_player():
                    self.battle.select_monster(player, monster)
                elif player == self.battle.get_opposing_player():
                    self.battle.try_attack(player, monster)
                break

        elif self.current_state == 'how_to_play':
            if self.back_button.is_hovered(pos):
                self.current_state = 'menu'


    def draw(self):
        self.screen.fill((21, 30, 61)) # TODO: Get color from config file

        if self.current_state == 'menu':
            self.draw_menu()
        elif self.current_state == 'game':
            self.card_rects = self.draw_game()
        elif self.current_state == 'how_to_play':
            self.draw_how_to_play()

    def draw_menu(self) -> None:
        self.start_button.draw(self.screen)
        self.how_to_button.draw(self.screen)
        self.quit_button.draw(self.screen)

    def draw_how_to_play(self) -> None:
        self.back_button.draw(self.screen)

        #TODO: add instructions. And add font to config, move instructions elsewhere as well
        font = pygame.font.SysFont('Arial', 40)
        text = font.render('How to play instructions will go here.....', 1, (0, 0, 0))

        self.screen.blit(text, (200,300))
        #self.screen.blit(text, (self.SCREEN_WIDTH / 2 - text.get_width() / 2, self.SCREEN_HEIGHT / 2 - text.get_height() / 2))

    def draw_game(self) -> list:
        card_rects = []  # For cards rectangle space

        card_width, card_height = 112, 220 #244, 150 This made it look centred even tho it wasn't
        space_between_cards = 10
        initial_x = 20
        initial_y = 80
        y_offset = card_height + 40

        turn = self.battle.current_turn

        if turn == Turn.PLAYER:
            turn_name = 'Player'
        else:
            turn_name = 'AI'

        info_font = pygame.font.SysFont('Arial', 24)
        turn_text = info_font.render(f'Turn: {turn_name}', True, (255, 255, 255))
        self.screen.blit(turn_text, (200, 28))

        for player, monsters in self.players.items():
            x_offset = 10  # Moves cards slightly away from the left
            for monster in monsters:

                if not monster.is_alive():
                    continue

                card_x = initial_x + x_offset
                card_y = initial_y + (player * y_offset)

                # create rect for card (used for clicking)
                card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
                card_rects.append((card_rect, player, monster))

                # draw card background
                pygame.draw.rect(self.screen, (50, 50, 50), card_rect) # COLOR: gray 50, 50, 50

                # Highlight selected card
                if monster == self.battle.selected_monster:
                    pygame.draw.rect(self.screen, (255,255,0), card_rect, 3) # bright yellow

                # load + scale monster image
                monster_img = self.get_monster_image(monster.image)

                image_rect = pygame.Rect(card_x + 16, card_y + 40, 80, 90)
                img_rect = monster_img.get_rect(center=image_rect.center)

                # center
                # img_x = card_x + (112 - 80) // 2
                # img_y = card_y + 40

                # draw text
                card_name_font = pygame.font.SysFont('Arial', 20, bold=False)
                name_text = card_name_font.render(f'{monster.name}', True, (255, 255, 255))

                hp_text_font = pygame.font.SysFont('Arial', 16)  # TODO: add font to config
                hp_text = hp_text_font.render(f'HP: {monster.hp}', True, (255, 255, 255))

                card_strength_font = pygame.font.SysFont('Arial', 16, bold=False)
                strength_text = card_strength_font.render(f'STR: {monster.strength}', True, (255, 255, 255))

                card_energy_font = pygame.font.SysFont('Arial', 16, bold=False)
                energy_text = card_energy_font.render(f'ENG: {monster.energy}', True, (255, 255, 255))

                # display monster's image and hp
                self.screen.blit(name_text, (card_x + 8, card_y + 8)) # Name
                self.screen.blit(monster_img, image_rect) # Image
                self.screen.blit(hp_text, (card_x + 8, card_y + 130)) #HP

                self.screen.blit(strength_text, (card_x + 8, card_y + 150))  # STR

                self.screen.blit(energy_text, (card_x + 8, card_y + 170))  # ENG

                x_offset += card_width + space_between_cards

            self.battle_log.draw(self.screen)

        return card_rects






