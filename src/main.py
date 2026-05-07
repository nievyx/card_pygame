"""
Main entry point for game.

Loads configuration data, creates game instance,
and starts main game loop.
"""

from src.utils.config import Config
from src.game.game_controller import Game

def main():
    Config.load_game_data()
    game = Game(config=Config())
    game.start()

if __name__ == '__main__':
    main()