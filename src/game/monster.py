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

        #TODO: Monsters will hold individual levels, and custom stats (owned monster class)

    def is_alive(self):
        return self.hp > 0

    def attack(self):
        pass

    def defense(self):
        pass

    def rest(self):
        pass

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        if self.hp <= 0:
            self.alive = False
