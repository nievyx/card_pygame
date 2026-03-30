import pygame
import random
import os
from src.ui.button import Button
from typing import Literal

pygame.init()

game_title = "Card Dealing Simulator!"
card_images = {}

State = Literal['menu', 'game', 'how_to_play', 'quit']
current_state: State = 'menu'

suits = ['c', 'd', 'h', 's']
ranks = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13']

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
    players[i] = [deck.pop() for _ in range(cards_per_player)]

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
def handle_mouse_click(pos, state: State) -> State:
    """
    Check where mouse button is clicked.
    Used on main menu to detect if user is clicking any of the buttons.
    :returns: New state based on mouse click event.
    """
    if state == 'menu':
        # Check if start button pressed
        if start_button.is_over(pos):
            return 'game'

        # Check if how_to_play button pressed
        if how_to_button.is_over(pos):
            return 'how_to_play'

        # Check if quit button pressed
        if quit_button.is_over(pos):
            return 'quit'

    # Check for if back button clicked
    elif state in ['game', 'how_to_play']:
        if back_button.is_over(pos):
            return 'menu'

    return state


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
                if start_button.is_over(pos):
                    current_state = 'game'
                elif how_to_button.is_over(pos):
                    pass #TODO: finish this



    screen.fill((0, 120, 0))

    # Menu Menu
    if current_state == 'menu':
        #TODO: All below should be put in a function
        start_button.draw(screen)

    # Game Loop
    elif current_state == 'game':
        card_width, card_height = 112, 150
        space_between_cards = 10
        initial_x = 20
        initial_y = 80
        y_offset = card_height + 40

        for player, cards in players.items():
            x_offset = 0
            for card in cards:
                screen.blit(
                    card_images[card],
                    (initial_x + x_offset, initial_y + (player * y_offset))
                )
                x_offset += card_width + space_between_cards

    pygame.display.flip()

pygame.quit()