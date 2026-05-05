import random

class Monster:
    monster_pool = {}

    def __init__(self, name, image, face, hp, mp, energy, strength, known_spells = None, rarity='common'):
        self.name = name
        self.image = image
        self.face = face
        self.hp = hp
        self.mp = mp
        self.strength = strength # Strength of physical damage
        self.energy = energy # Points needed for monsters to physical attack?

        self.max_hp = self.hp
        self.max_mp = self.mp
        self.max_energy = self.energy
        self.max_strength = self.strength

        self.dropped_exp = 10 #Placeholder

        self.known_spells = known_spells if known_spells is not None else []
        self.rarity = rarity

        # print(f"CREATED: {name} rarity={rarity}")

    @classmethod
    def register(cls, monster):
        cls.monster_pool[monster.name] = monster

    @classmethod
    def generate_rand_team(cls, size=5, rarity_weights=None):
        if rarity_weights:
            weights = [rarity_weights[monster.rarity] for monster in cls.monster_pool.values()]
            team = random.choices(list(cls.monster_pool.values()), weights=weights, k=size)
        else:
            team = random.choices(list(cls.monster_pool.values()), k=size)

        return [monster.clone() for monster in team]

    @classmethod
    def generate_rand_monster(cls, rarity_weights=None):
        size=1
        pool = list(cls.monster_pool.values())

        if rarity_weights:
            weights = [rarity_weights[monster.rarity] for monster in pool]
            new_card = random.choices(pool, weights=weights, k=size)[0]
        else:
            new_card = random.choices(pool, k=1)[0]

        return new_card.clone()


    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def reset(self):
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.energy = self.max_energy
        self.strength = self.max_strength

    def clone(self):
        return Monster(
            self.name,
            self.image,
            self.face,
            self.hp,
            self.mp,
            self.energy,
            self.strength,
            known_spells=list(self.known_spells),
            rarity=self.rarity
        )

    def deplete_energy(self, amount: int) -> None:
        self.energy = max(0, self.energy - amount)

    def recover_energy(self, amount: int) -> None:
        self.energy = min(0, self.energy + amount)

    def attack(self, target) -> int:
        if not self.can_attack():
            raise ValueError(f'{self.name} has no energy left to fight')
            #TODO: remove error and just let monster not fight, u may also need to update logic for enemy using a monster with no energy
             #TODO: Append to battle log?, probably not here

        #TODO: update generate msg in battle log to say critial hit
        roll = random.randint(1, 6)
        if roll > 4:
            test_crit = 1
        else:
            test_crit = 0

        damage = self.strength
        if test_crit:
            damage = round(self.strength * self.critical_hit())

        self.deplete_energy(1) #TODO: change amount?
        target.take_damage(damage)

        return damage

    def critical_hit(self) -> float:
        modifier = random.uniform(2.2, 3.3)
        return modifier

    def can_attack(self) -> bool:
        return self.energy > 0

    def defense(self):
        pass

    def rest(self):
        pass

    def take_damage(self, amount:int) -> int:
        starting_hp = self.hp

        self.hp = max(0, self.hp - amount)

        return starting_hp + amount

    def restore_health(self, amount:int):
        """restore the health of the monster
        :returns: amount of health healed"""
        if self.is_alive:

            if amount <= 0:
                return 0

            starting_hp = self.hp
            self.hp = min(self.max_hp, self.hp + amount)
            return self.hp - starting_hp
        return None






