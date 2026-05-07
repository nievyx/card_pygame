"""

DEBUG

"""

from src.utils.config import Config
from src.game.game_controller import Game

def debug_battle():
    Config.load_game_data()
    game = Game(config=Config())

    game.debug_mode = True

    game.start()


if __name__ == "__main__":
    try:
        debug_battle()
    except FileNotFoundError as e:
        print(f'Error: {e}')
        print('Run via: \npython -m src.debug.battle')