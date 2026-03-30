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

    def is_alive(self):
        return self.hp > 0

    def attack(self):
        pass

    def defense(self):
        pass

    def rest(self):
        pass

