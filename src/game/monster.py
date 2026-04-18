import random

class Monster:
    monster_pool = []

    def __init__(self, name, image, hp, mp, energy, strength, known_spells = None, rarity='common'):
        self.name = name
        self.image = image
        self.hp = hp
        self.mp = mp
        self.strength = strength # Strength of physical damage
        self.energy = energy # Points needed for monsters to physical attack?

        self.max_hp = self.hp
        self.max_mp = self.mp
        self.max_energy = self.energy
        self.max_strength = self.strength
        self.alive = True

        self.dropped_exp = 10 #Placeholder

        self.known_spells = known_spells if known_spells is not None else []
        self.rarity = rarity

        Monster.monster_pool.append(self)

        # print(f"CREATED: {name} rarity={rarity}")

    @classmethod
    def get_monster_pool(cls):
        return cls.monster_pool

    def is_alive(self):
        return self.hp > 0

    def deplete_energy(self, amount: int) -> None:
        self.energy = max(0, self.energy - amount)

    def attack(self, target) -> int:
        if not self.can_attack():
            raise ValueError(f'{self.name} has no energy left to fight') #TODO: remove error and just let monster not fight, u may also need to update logic for enemy using a monster with no energy
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

        self.deplete_energy(1) #TODO: change to strength, when changed to str moves can be used even if at least 1 strength this not correct
        target.take_damage(damage)

        return damage

    def critical_hit(self) -> float:
        modifier = random.uniform(2.2, 3.3)
        return modifier

    def can_attack(self) -> bool:
        """ #TODO: update this when decided how much energy attacks will use"""
        return self.energy > 0

    def defense(self):
        pass

    def rest(self):
        pass

    def check_is_alive(self):
        if self.hp <= 0:
            self.alive = False

    def take_damage(self, amount):
        starting_hp = self.hp

        self.hp = max(0, self.hp - amount)
        self.check_is_alive()

        return starting_hp + amount

    def restore_health(self, amount):
        """restore the health of the monster
        :returns: amount of health healed"""
        self.check_is_alive()

        if amount <= 0:
            return 0

        starting_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - starting_hp




