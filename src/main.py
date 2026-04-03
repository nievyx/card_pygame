from src.config import Config
from src.game.game import Game

def main():
    game = Game(config=Config())
    game.start()

if __name__ == '__main__':
    main()