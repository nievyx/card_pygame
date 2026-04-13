from src.data.spells import light_heal, fireball, ice_bolt
from src.game.monster import Monster
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MONSTER_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'assets', 'monsters'))

chimera = Monster(
        name='Chimera',
        image=MONSTER_DIR + '/Chimera.png',
        hp=12,
        mp=10,
        energy=5,
        strength=4,
        known_spells = [fireball]
)
demon = Monster(
        name='Demon',
        image=MONSTER_DIR + '/Demon.png',
        hp=15,
        mp=6,
        energy=8,
        strength=9,
        known_spells = [ice_bolt]
)
calm = Monster(
        name='Calm',
        image=MONSTER_DIR + '/Calm.png',
        hp=10,
        mp=6,
        energy=6,
        strength=3,
        known_spells = [light_heal]
)
yanpi = Monster(
        name='Yanpi',
        image=MONSTER_DIR + '/Yanpi.png',
        hp=8,
        mp=7,
        energy=5,
        strength=2,
        known_spells = [light_heal]
)
fury = Monster('Fury', MONSTER_DIR + '/Fury.png',6,7,5,9,[fireball])

djinn = Monster('Djinn', MONSTER_DIR + '/djinn.png',7,7,6,7,[ice_bolt])