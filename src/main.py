import pygame
import random
import os
from src.ui import Button # re-exported via package for cleaner imports
from src.game.monster import Monster #TODO: make import cleaner via __init__.py
from typing import Literal

pygame.init() # Keep at top, before any game setup etc.

# Paths
#TODO: connect to loading assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.abspath(os.path.join(BASE_DIR, '..','cards'))

game_title = "Card Dealing Simulator!"

# Monster Creation
# TODO: move these to monsters.py
# Images currently in assets/monsters dir
# TODO : fix image mess
MONSTER_DIR = os.path.abspath(os.path.join(BASE_DIR, '..','assets/monsters'))
Chimera = Monster(name= 'Chimera', image = MONSTER_DIR + '/chimera.png', hp = 12, mp = 8, energy=5, strength=4 )
Demon = Monster(name = 'Demon', image =  MONSTER_DIR + '/demon.png', hp = 15, mp = 4, energy=8, strength=9 )
monster_pool = [Chimera, Demon] #TODO: add auto list creation in class


State = Literal['menu', 'game', 'how_to_play', 'quit']
current_state: State = 'menu'

suits = ['c', 'd', 'h', 's']
ranks = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13']

# Load assets
card_images = {}
for suit in suits:
    for rank in ranks:
        image_path = os.path.join('..\cards', f'{suit}{rank}.png')
        original_image = pygame.image.load(image_path)
        scaled_image = pygame.transform.scale(original_image, (112, 150))
        card_images[(suit, rank)] = scaled_image

deck = [(suit, rank) for suit in suits for rank in ranks]
random.shuffle(deck)

num_players = 2
cards_per_player = 5
players = {}

for i in range(num_players):
    # players[i] = [deck.pop() for _ in range(cards_per_player)] # Old
    players[i] = [ # TODO: better to create a reset monster in class, this looks messy
        Monster(m.name, m.image, m.hp, m.mp, m.energy, m.strength)
        for m in random.choices(monster_pool, k=cards_per_player)
    ]

screen_width = 1200
screen_height = 850

screen = pygame.display.set_mode((screen_width, screen_height))
#Game Title
pygame.display.set_caption(game_title)

#Button Creation
start_button = Button((0,255,0), 400,150,200,80,"Start")
how_to_button = Button((0,0,255), 400,300,200,80,"How To Play")
quit_button = Button((255,0,0), 400,450,200,80,"Quit")
back_button = Button((200, 200, 200), 20, 20, 150, 60, "Back")

# TODO : this is unused!
def handle_mouse_click(mouse_pos, state: State) -> State:
    """
    Check where mouse button is clicked.
    Used on main menu to detect if user is clicking any of the buttons.
    :returns: New state based on mouse click event.
    """
    if state == 'menu':
        # Check if start button pressed
        if start_button.is_hovered(mouse_pos):
            return 'game'

        # Check if how_to_play button pressed
        if how_to_button.is_hovered(mouse_pos):
            return 'how_to_play'

        # Check if quit button pressed
        if quit_button.is_hovered(mouse_pos):
            return 'quit'

    # Check for if back button clicked
    elif state in ['game', 'how_to_play']:
        if back_button.is_hovered(mouse_pos):
            return 'menu'

    return state

def how_to_play():
    screen.fill((255, 255, 255)) # White
    font = pygame.font.SysFont('Arial', 40)  # TODO : Create font variables
    text = font.render('How to play instructions will go here.....', 1, (0, 0, 0))
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2))

running = True
while running:
    for event in pygame.event.get():

        # Check if user wants to quit
        if event.type == pygame.QUIT:
            running = False

        #Logic for clicking menu buttons
        # TODO: Add game, how_to
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # TODO: run handle mouse click function here

            # ❌ This is about to be removed
            if current_state == 'menu':
                if start_button.is_hovered(pos):
                    current_state = 'game'
                elif how_to_button.is_hovered(pos):
                    pass #TODO: finish this
                    current_state = 'how_to_play'


    screen.fill((0, 120, 0)) # Green

    # Menu Menu
    if current_state == 'menu':
        #TODO: move to main menu function
        start_button.draw(screen)
        how_to_button.draw(screen)

    # How to play screen
    elif current_state == 'how_to_play':
        how_to_play()

    # Game Loop
    elif current_state == 'game':
        card_width, card_height = 112, 150
        space_between_cards = 10
        initial_x = 20
        initial_y = 80
        y_offset = card_height + 40

        # Old
        # for player, cards in players.items():
        #     x_offset = 0
        #     for card in cards:
        #         screen.blit(
        #             card_images[card],
        #             (initial_x + x_offset, initial_y + (player * y_offset))
        #         )
        #         x_offset += card_width + space_between_cards

        for player, monsters in players.items():
            x_offset = 0
            for monster in monsters:
                card_x = initial_x + x_offset
                card_y = initial_y + (player * y_offset)

                # Draw temp card background
                pygame.draw.rect(screen, (50,50,50), (card_x, card_y, 112, 150))

                # load + scale monster image
                monster_img = pygame.image.load(monster.image)
                monster_img = pygame.transform.scale(monster_img, (80, 90))

                # center
                img_x = card_x + (112 - 80) // 2
                img_y = card_y + 40

                screen.blit(monster_img, (img_x, img_y))

                x_offset += card_width + space_between_cards

    # Update display to reflect changes
    pygame.display.flip()

pygame.quit() #TODO: Will need a quit function