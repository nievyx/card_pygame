"""
This is not in use.

Player creation is handled via config and Player and AI are currently managed as indexes,
in the battle system, where 0 represents the player and 1 represents the enemy AI.
"""

class Player:
    def __init__(self, name: str, monsters=None, is_human=True) -> None:
        self.name = name
        self.is_human = is_human

        # All owned monsters
        self.monsters = list(monsters) if monsters else [] # Cards owned and collected by the player

        # Player Stats
        self.gold = 0

    def get_alive_monsters(self):
        return [monster for monster in self.monsters if monster.is_alive()]

    def has_alive_monsters(self):
        return len(self.get_alive_monsters()) > 0

class AI:
    def __init__(self):
        self.name = 'AI'

class OwnedMonster:
    def __init__(self, monster) -> None:
        self.monster = monster
        self.level = 1
        self.nickname = None


