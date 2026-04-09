import random
from src.game import Monster

PLAYER_LOG_COLOR = (0, 255, 255)
ENEMY_LOG_COLOR = (240, 80, 16)

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



