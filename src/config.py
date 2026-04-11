import os
import random

import pygame

from src.game import Monster

PLAYER_LOG_COLOR = None
ENEMY_LOG_COLOR = (240, 80, 16)
# Note: theme/theme.py replacing this in future implementation

class Config:
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 850
    game_title = "Niamh's Monster Cards"

    @staticmethod
    def load_game_data():
        """
        Loads all game data via import side effects.
        Registers monsters and spells in global pools.
        NOTE: Imports may appear to be unused in some IDEs, but
        is required.
        """
        import src.data.monsters
        import src.data.spells

    @staticmethod
    def load_random_background(screen_size):
        folder = 'assets/backgrounds/'
        img_types = ('.png', '.jpg', '.jpeg', '.webp')

        files = [
            os.path.join(folder, name)
            for name in os.listdir(folder)
            if name.lower().endswith(img_types)
        ]
        bg_img = random.choice(files)

        image = pygame.image.load(bg_img).convert()
        image = pygame.transform.scale(image, screen_size)

        return image

    def create_players(self):
        num_players = 2
        cards_per_player = 5
        players = {}

        for i in range(num_players):
            players[i] = [
                Monster(m.name, m.image, m.hp, m.mp, m.energy, m.strength, known_spells=list(m.known_spells))
                for m in random.choices(Monster.monster_pool, k=cards_per_player)
            ]
        return players




