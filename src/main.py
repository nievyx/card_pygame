"""
Main entry point for game.

Loads configuration data, creates game instance,
and starts main game loop.
"""

from src.utils.config import Config
from src.game.game_controller import Game

def create_game():
    Config.load_game_data()
    return Game(config=Config())

def main():
    game = create_game()
    game.start()

async def main_async():
    """
    Main entry point for Pygbag async game.
    (Browser Version)
    """
    game = create_game()
    await game.start_async()

if __name__ == '__main__':
    main()