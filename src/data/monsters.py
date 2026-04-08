from src.game.monster import Monster
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MONSTER_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'assets', 'monsters'))

chimera = Monster(
            name='Chimera',
            image=MONSTER_DIR + '/Chimera.png',
            hp=12,
            mp=8,
            energy=5,
            strength=4
)
demon = Monster(
        name='Demon',
        image=MONSTER_DIR + '/Demon.png',
        hp=15,
        mp=4,
        energy=8,
        strength=9
)
calm = Monster(
        name='Calm',
        image=MONSTER_DIR + '/Calm.png',
        hp=10,
        mp=6,
        energy=6,
        strength=3
)

monster_pool = [chimera, demon, calm]  # TODO: add auto list creation in class