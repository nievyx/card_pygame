from src.content.spell_data import light_heal, fireball, ice_bolt, mid_heal, ice_shards, vine_attack, strong_heal, fire_blast
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
        face=FACE_DIR + '/Calm.png',
        hp=10,
        mp=6,
        energy=6,
        strength=3,
        known_spells = [light_heal]
))
Monster.register(Monster(
        name='Yanpi',
        image=MONSTER_DIR + '/Yanpi.png',
        face=FACE_DIR + '/Yanpi.png',
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
        face=FACE_DIR + '/Yanfly.png',
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
Monster.register(Monster(
    name='Brain Slime',
    image=MONSTER_DIR + '/Brain Slime 2.png',
    face=FACE_DIR + '/Brain Slime 2.png',
    hp=9,
    mp=8,
    energy=5,
    strength=4,
    known_spells=[ice_shards],
    rarity='uncommon'
))

Monster.register(Monster(
    name='Coward',
    image=MONSTER_DIR + '/Coward.png',
    face=FACE_DIR + '/Coward.png',
    hp=6,
    mp=4,
    energy=7,
    strength=3,
    known_spells=[],
    rarity='common'
))

Monster.register(Monster(
    name='Crow',
    image=MONSTER_DIR + '/Crow.png',
    face=FACE_DIR + '/Crow.png',
    hp=7,
    mp=6,
    energy=8,
    strength=5,
    known_spells=[],
    rarity='common'
))

Monster.register(Monster(
    name='Dragon Hawk',
    image=MONSTER_DIR + '/Dragon Hawk.png',
    face=FACE_DIR + '/Dragon Hawk.png',
    hp=10,
    mp=8,
    energy=8,
    strength=7,
    known_spells=[fireball],
    rarity='rare'
))

Monster.register(Monster(
    name='Drakee',
    image=MONSTER_DIR + '/Drakee.png',
    face=FACE_DIR + '/Drakee.png',
    hp=8,
    mp=5,
    energy=8,
    strength=5,
    known_spells=[],
    rarity='common'
))

Monster.register(Monster(
    name='Emp. Slime',
    image=MONSTER_DIR + '/Emperor Slime.png',
    face=FACE_DIR + '/Emperor Slime.png',
    hp=14,
    mp=10,
    energy=5,
    strength=6,
    known_spells=[light_heal, mid_heal],
    rarity='rare'
))

Monster.register(Monster(
    name='Evil God',
    image=MONSTER_DIR + '/evilGod.png',
    face=FACE_DIR + '/evilGod.png',
    hp=18,
    mp=12,
    energy=7,
    strength=12,
    known_spells=[fire_blast],
    rarity='legendary'
))

Monster.register(Monster(
    name='Flaming Snowman',
    image=MONSTER_DIR + '/Flaming Snowman.png',
    face=FACE_DIR + '/Flaming Snowman.png',
    hp=10,
    mp=9,
    energy=6,
    strength=7,
    known_spells=[fireball, ice_bolt],
    rarity='rare'
))

Monster.register(Monster(
    name='Octopot',
    image=MONSTER_DIR + '/octopot.png',
    face=FACE_DIR + '/octopot.png',
    hp=8,
    mp=6,
    energy=6,
    strength=5,
    known_spells=[ice_shards],
    rarity='common'
))

Monster.register(Monster(
    name='Old Turtle',
    image=MONSTER_DIR + '/Old Turtle.png',
    face=FACE_DIR + '/Old Turtle.png',
    hp=14,
    mp=4,
    energy=3,
    strength=6,
    known_spells=[strong_heal],
    rarity='uncommon'
))

Monster.register(Monster(
    name='Skeleton',
    image=MONSTER_DIR + '/Skeleton.png',
    face=FACE_DIR + '/Skeleton.png',
    hp=9,
    mp=3,
    energy=6,
    strength=8,
    known_spells=[fireball],
    rarity='common'
))

Monster.register(Monster(
    name='Wave Slime',
    image=MONSTER_DIR + '/Wave Slime.png',
    face=FACE_DIR + '/Wave Slime.png',
    hp=8,
    mp=8,
    energy=6,
    strength=4,
    known_spells=[ice_bolt],
    rarity='common'
))

Monster.register(Monster(
    name='Yanflayer',
    image=MONSTER_DIR + '/Yanflayer.png',
    face=FACE_DIR + '/Yanflayer.png',
    hp=10,
    mp=9,
    energy=8,
    strength=5,
    known_spells=[light_heal, mid_heal],
    rarity='rare'
))