import os
import random

from src.game.monster import Monster #TODO: make import cleaner via __init__.py

PLAYER_LOG_COLOR = None # AQUA (0, 255, 255)
ENEMY_LOG_COLOR = (255, 0, 0)

class Config:
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 850
    game_title = "Niamh's Monster Cards"

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MONSTER_DIR = os.path.abspath(os.path.join(BASE_DIR, 'assets', 'monsters'))

    def create_players(self):
        chimera = Monster(
            name='Chimera',
            image=self.MONSTER_DIR + '/chimera.png',
            hp=12,
            mp=8,
            energy=5,
            strength=4
)
        demon = Monster(
            name='Demon',
            image=self.MONSTER_DIR + '/demon.png',
            hp=15,
            mp=4,
            energy=8,
            strength=9
)
        calm = Monster(
            name='Calm',
            image=self.MONSTER_DIR + '/calm.png',
            hp=10,
            mp=6,
            energy=6,
            strength=3
        )

        monster_pool = [chimera, demon, calm]  # TODO: add auto list creation in class

        num_players = 2
        cards_per_player = 5
        players = {}

        for i in range(num_players):
            players[i] = [
                Monster(m.name, m.image, m.hp, m.mp, m.energy, m.strength)
                for m in random.choices(monster_pool, k=cards_per_player)
            ]
        return players
