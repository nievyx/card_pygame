import pygame
import random
import os
from src.ui import Button # re-exported via package for cleaner imports
from src.game.monster import Monster #TODO: make import cleaner via __init__.py
from src.game.battle import Battle #TODO: also make import cleaner via __init__.py
from typing import Literal

pygame.init() # Keep at top, before any game setup etc.

# Paths # TODO: connect to loading assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.abspath(os.path.join(BASE_DIR, '..','cards'))

game_title = "Niamh's Monster Cards"

how_to_bg = (21,30,61)

# Monster Creation
# TODO: move these to data/monsters.py
# Images currently in assets/monsters dir
# TODO : fix image mess
MONSTER_DIR = os.path.abspath(os.path.join(BASE_DIR, '..','assets/monsters'))
Chimera = Monster(name= 'Chimera', image = MONSTER_DIR + '/chimera.png', hp = 12, mp = 8, energy=5, strength=4 )
Demon = Monster(name = 'Demon', image =  MONSTER_DIR + '/demon.png', hp = 15, mp = 4, energy=8, strength=9 )
monster_pool = [Chimera, Demon] #TODO: add auto list creation in class


State = Literal['menu', 'game', 'how_to_play', 'quit']


num_players = 2 # TODO: Update this
cards_per_player = 5
players = {}

for i in range(num_players):
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
how_to_button = Button((0,0,255), 400,300,420,80,"How To Play")
quit_button = Button((170,90,10), 400,450,200,80,"Quit") # TODO: not in use
back_button = Button((200, 200, 200), 20, 20, 150, 60, "Back")
main_menu_button =  Button((200, 200, 200), 20, 20, 150, 60, "Menu") #TODO: dummy button


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
    elif state in ('game', 'how_to_play'):
        if back_button.is_hovered(mouse_pos):
            return 'menu'

    return state

def how_to_play():
    # screen.fill(how_to_bg) # White 255,255,255
    font = pygame.font.SysFont('Arial', 40)  # TODO : Create font variables
    text = font.render('How to play instructions will go here.....', 1, (0, 0, 0))
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2))

    #TODO: render back button
    back_button.draw(screen)

def draw_game():
    card_width, card_height = 244, 150
    space_between_cards = 10
    initial_x = 20
    initial_y = 80
    y_offset = card_height + 40

    for player, monsters in players.items():
        x_offset = 0
        for monster in monsters:
            card_x = initial_x + x_offset
            card_y = initial_y + (player * y_offset)

            # Draw card background
            pygame.draw.rect(screen, (50, 50, 50), (card_x, card_y, 112, 150))

            # load + scale monster image
            monster_img = pygame.image.load(monster.image)
            monster_img = pygame.transform.scale(monster_img, (80, 90))

            # center
            img_x = card_x + (112 - 80) // 2
            img_y = card_y + 40

            # draw text
            #card_name_font = pygame.font.SysFont('Arial', 20, bold=True) #TODO: move higher up
            hp_text_font = pygame.font.SysFont('Arial', 16) #TODO: move higher up

            hp_text = hp_text_font.render(f'HP: {monster.hp}', True, (255, 255, 255))

            screen.blit(hp_text, (card_x +8, card_y + 8))

            #NOTE: If you want cards centered in screen
            # x_offset += card_width + space_between_cards # was not right delete, change card_ width to 122 -> 244







            screen.blit(monster_img, (img_x, img_y))

            x_offset += card_width + space_between_cards

def quit_game():
    pygame.quit()

def main():
    current_state: State = 'menu'

    running = True
    while running:

        for event in pygame.event.get():

            # Check if user wants to quit
            if event.type == pygame.QUIT:
                running = False

            #Logic for clicking menu buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                current_state = handle_mouse_click(pos, current_state)



        screen.fill((21,30,61)) # Blue 21,30,61 # Green 0,120,10

        # Menu Menu
        if current_state == 'menu':
            #TODO: move to main menu function
            start_button.draw(screen)
            how_to_button.draw(screen)
            quit_button.draw(screen)

        # How to play screen
        elif current_state == 'how_to_play':
            how_to_play()

        # Game Loop
        elif current_state == 'game':
            draw_game()

        # Update display to reflect changes
        pygame.display.flip()

    quit_game()

if __name__ == '__main__':
    main()