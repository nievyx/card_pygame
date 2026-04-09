import random

from src.game.monster import Monster #TODO: make import cleaner via __init__.py
import src.data.monsters # This being used to create monster pool (even tho ide can't recognise that)
# ^ TODO: probs put this in main
import src.data.spells

PLAYER_LOG_COLOR = None # AQUA (0, 255, 255)
ENEMY_LOG_COLOR = (240, 80, 16)

class Config:
    SCREEN_WIDTH = 1200 # TODO: Game set to fullscreen via game.py
    SCREEN_HEIGHT = 850
    game_title = "Niamh's Monster Cards"

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
