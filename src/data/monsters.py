from src.data.spells import light_heal, fireball, ice_bolt, mid_heal, ice_shards, vine_attack, strong_heal, fire_blast
from src.game.monster import Monster
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MONSTER_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'assets', 'monsters'))
FACE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'assets', 'monsters', 'faces'))

Monster.register(Monster(
        name='Chimera',
        image=MONSTER_DIR + '/Chimera.png',
        face=FACE_DIR + '/Chimera.png',
        hp=12,
        mp=10,
        energy=5,
        strength=4,
        known_spells = [fireball]
))
Monster.register(Monster(
        name='Demon',
        image=MONSTER_DIR + '/Demon.png',
        face=FACE_DIR + '/Demon.png',
        hp=15,
        mp=6,
        energy=8,
        strength=9,
        known_spells = [ice_bolt, ice_shards]
))
Monster.register(Monster(
        name='Calm',
        image=MONSTER_DIR + '/Calm.png',
        face=FACE_DIR + '/Demon.png',
        hp=10,
        mp=6,
        energy=6,
        strength=3,
        known_spells = [light_heal]
))
Monster.register(Monster(
        name='Yanpi',
        image=MONSTER_DIR + '/Yanpi.png',
        face=FACE_DIR + '/Demon.png',
        hp=8,
        mp=7,
        energy=5,
        strength=2,
        known_spells = [light_heal]
))
yanpi = Monster.monster_pool["Yanpi"]
Monster.register(Monster(
        name='Yanfly',
        image=MONSTER_DIR + '/Yanfly.png',
        face=FACE_DIR + '/Demon.png',
        hp=yanpi.max_hp+3,
        mp=yanpi.max_mp+4,
        energy=yanpi.max_energy+2,
        strength=yanpi.max_strength+2,
        known_spells = [light_heal, mid_heal],
        rarity='uncommon'
))
Monster.register(Monster(
    'Fury',
    MONSTER_DIR + '/Fury.png',
    FACE_DIR + '/Fury.png',
    6, 7, 5, 9,
    [fireball],
))

Monster.register(Monster(
    'Earth King',
    MONSTER_DIR + '/Earth King.png',
    FACE_DIR + '/Earth King.png',
    7, 7, 6, 7,
    [ice_bolt],
    'uncommon',
))

Monster.register(Monster(
    'Djinn',
    MONSTER_DIR + '/djinn.png',
    FACE_DIR + '/djinn.png',
    7, 7, 6, 7,
    [ice_bolt],
    'rare',
))

Monster.register(Monster(
    'Plant',
    MONSTER_DIR + '/plant.png',
    FACE_DIR + '/plant.png',
    7, 7, 6, 7,
    [vine_attack],
    'uncommon',
))
Monster.register(Monster(
        name='Behemoth',
        image=MONSTER_DIR + '/Behemoth.png',
        face= FACE_DIR + '/Behemoth.png',
        hp=yanpi.max_hp+13,
        mp=yanpi.max_mp+14,
        energy=yanpi.max_energy+8,
        strength=yanpi.max_strength+12,
        rarity='legendary'
))
Monster.register(Monster(
        name='Dark Angel',
        image=MONSTER_DIR + '/Angel of the Dark.png',
        face=FACE_DIR + '/Angel of the Dark.png',
        hp=yanpi.max_hp+5,
        mp=yanpi.max_mp+2,
        energy=yanpi.max_energy+5,
        strength=yanpi.max_strength+6,
        known_spells = [light_heal, mid_heal],
        rarity='rare'
))
Monster.register(Monster(
        name='Blue Dragon',
        image=MONSTER_DIR + '/Blue Dragon.png',
        face=FACE_DIR + '/Blue Dragon.png',
        hp=yanpi.max_hp+13,
        mp=yanpi.max_mp+14,
        energy=yanpi.max_energy+8,
        strength=yanpi.max_strength+15,
        known_spells = [light_heal, mid_heal, strong_heal, fireball, fire_blast],
        rarity='legendary'
))