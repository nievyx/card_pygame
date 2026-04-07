class Monster:
    def __init__(self, name, image, hp, mp, energy, strength ):
        self.name = name
        self.image = image
        self.hp = hp
        self.mp = mp
        self.strength = strength # Strength of physical damage
        self.energy = energy # Points needed for monsters to physical attack

        self.max_hp = self.hp
        self.max_mp = self.mp
        self.alive = True

        #TODO: Monsters will hold individual levels, and custom stats (owned monster class, this is in player class)

    def is_alive(self):
        return self.hp > 0

    def deplete_energy(self, amount: int) -> None:
        self.energy = max(0, self.energy - amount)

    def attack(self, target) -> int:
        if not self.can_attack():
            raise ValueError(f'{self.name} has no energy left to fight') #TODO: Append to battle log?

        damage = self.strength

        self.deplete_energy(1) #TODO: change to strength
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


