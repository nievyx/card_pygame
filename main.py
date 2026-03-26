import pygame
import random
import os
 
pygame.init()
 
 
card_images = {}
 
suits = ['c', 'd', 'h', 's']
 
ranks = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13']
 
for suit in suits:
    for rank in ranks:
        image_path = os.path.join('cards/' f'{suit}{rank}.png')
        original_image = pygame.image.load(image_path)
        scaled_image = pygame.transform.scale(original_image, (112,150))
 
deck = [(suit,rank) for suit in suits for rank in ranks]
random.shuffle(deck)
 
num_players = 4
 
cards_per_player = 5
 
players = {}
 
for i in range(num_players):
    players[i] = [deck.pop() for _ in range(cards_per_player)]
 
screen_width = 1200 
screen_height = 800
 
screen = pygame.display.set.mode((screen_width, screen_height))
pygame.display.set_caption("Card Dealing Simulator")
 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
    screen.fill((0, 120, 0))
 
    card_width, card_hight = 112, 159
    space_between_cards = 10 
    initial_x = 20
    initial_y = 80
    y_offset = card_hight + 40
 
    for player, cards in player.items():
        x_offset = 0 
        for card in cards:
            screen.blit(card_images[card], (initial_x + x_offset, initial_y + (player * y_offset)))
            x_offset += card_width + space_between_cards
 
        pygame.display.flip()
    pygame.quit()