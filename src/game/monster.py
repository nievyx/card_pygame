class Monster:
    monster_pool = []

    def __init__(self, name, image, hp, mp, energy, strength, known_spells = None):
        self.name = name
        self.image = image
        self.hp = hp
        self.mp = mp
        self.strength = strength # Strength of physical damage
        self.energy = energy # Points needed for monsters to physical attack

        self.max_hp = self.hp
        self.max_mp = self.mp
        self.alive = True

        self.dropped_exp = 10 #Placeholder

        #TODO: future: add a requirement to fill like level 5, hp above 20 (if u want to pick upgrades)
        self.known_spells = known_spells if known_spells is not None else []

        Monster.monster_pool.append(self)

        #TODO: Monsters will hold individual levels, and custom stats (owned monster class, this is in player class)

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

        damage = self.strength

        self.deplete_energy(1) #TODO: change to strength, when changed to str moves can be used even if at least 1 strength this not correct
        target.take_damage(damage)

        return damage

    def critical_hit(self, target):
        pass

    def can_attack(self) -> bool:
        """ #TODO: update this when decided how much energy attacks will use"""
        return self.energy > 0

    def defense(self):
        pass

    def rest(self):
        pass

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        if self.hp <= 0:
            self.alive = False


