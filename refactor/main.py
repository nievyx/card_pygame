
import random
import os
from src.ui import Button # re-exported via package for cleaner imports
from src.game.monster import Monster #TODO: make import cleaner via __init__.py



# Paths # TODO: connect to loading assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.abspath(os.path.join(BASE_DIR, '..','cards'))

game_title = "Niamh's Monster Cards"

how_to_bg = (21,30,61)

# Monster Creation
# TODO: move these to data/monsters.py
# Images currently in assets/monsters dir
# TODO : fix image mess
MONSTER_DIR = os.path.abspath(os.path.join(BASE_DIR, '..','assets/monsters'))
Chimera = Monster(name= 'Chimera', image = MONSTER_DIR + '/chimera.png', hp = 12, mp = 8, energy=5, strength=4 )
Demon = Monster(name = 'Demon', image =  MONSTER_DIR + '/demon.png', hp = 15, mp = 4, energy=8, strength=9 )
monster_pool = [Chimera, Demon] #TODO: add auto list creation in class



cards_per_player = 5


for i in range(num_players):
    players[i] = [ # TODO: better to create a reset monster in class, this looks messy
        Monster(m.name, m.image, m.hp, m.mp, m.energy, m.strength)
        for m in random.choices(monster_pool, k=cards_per_player)
    ]

screen_width = 1200
screen_height = 850

