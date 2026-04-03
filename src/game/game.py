import pygame
from typing import Literal
from src.game.battle import Battle #TODO: also make import cleaner via __init__.py
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

        # Button Creation
        self.start_button = Button((0, 255, 0), 400, 150, 200, 80, "Start")
        self.how_to_button = Button((0, 0, 255), 400, 300, 420, 80, "How To Play")
        self.quit_button = Button((170, 90, 10), 400, 450, 200, 80, "Quit")
        self.back_button = Button((200, 200, 200), 20, 20, 150, 60, "Back")
        self.main_menu_button = Button((200, 200, 200), 20, 20, 150, 60, "Menu")

    def start(self) -> None:
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()

        pygame.quit()

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

            for rect, player, monster in self.card_rects:
                if rect.collidepoint(pos):
                    self.battle.selected_monster = monster
                    monster.hp = max(0, monster.hp - 1)  # TODO: placeholder -1 damage
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

    def draw_game(self) -> list:
        card_rects = []  # For cards rectangle space

        card_width, card_height = 112, 150 #244, 150
        space_between_cards = 10
        initial_x = 20
        initial_y = 80
        y_offset = card_height + 40

        for player, monsters in self.players.items():
            x_offset = 10  # Moves cards slightly away from the left
            for monster in monsters:
                card_x = initial_x + x_offset
                card_y = initial_y + (player * y_offset)

                # create rect for card (used for clicking)
                card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
                card_rects.append((card_rect, player, monster))

                # draw card background
                pygame.draw.rect(self.screen, (50, 50, 50), card_rect)

                # 🆕 New feature, highlight selected card
                if monster == self.battle.selected_monster:
                    pygame.draw.rect(self.screen, (255,255,0), card_rect, 3) # bright yellow

                # load + scale monster image
                monster_img = pygame.image.load(monster.image)
                monster_img = pygame.transform.scale(monster_img, (80, 90))

                # center
                img_x = card_x + (112 - 80) // 2
                img_y = card_y + 40

                # draw text
                # card_name_font = pygame.font.SysFont('Arial', 20, bold=True) #TODO: add monster name or nickname

                hp_text_font = pygame.font.SysFont('Arial', 16)  # TODO: add font to config
                hp_text = hp_text_font.render(f'HP: {monster.hp}', True, (255, 255, 255))

                # display monster's image and hp
                self.screen.blit(hp_text, (card_x + 8, card_y + 8))
                self.screen.blit(monster_img, (img_x, img_y))

                x_offset += card_width + space_between_cards

        return card_rects






