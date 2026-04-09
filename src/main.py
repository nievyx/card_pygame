from src.config import Config
from src.game.game import Game

def main():
    Config.load_game_data()
    game = Game(config=Config())
    game.start()

if __name__ == '__main__':
    main()