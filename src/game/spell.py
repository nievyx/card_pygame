import random

class Spell:
    spell_pool = []

    def __init__(self,
                 name: str,
                 strength: int,
                 mana_cost: int,
                 icon='',
                 use_in_overworld: bool = False
                 ):
        self.name = name
        self.strength = strength
        self.mana_cost = mana_cost
        self.icon = icon
        self.use_in_overworld = use_in_overworld

        Spell.spell_pool.append(self)

    def can_cast(self, caster) -> bool:
        return getattr(caster, 'mp', 0) >= self.mana_cost and caster.is_alive()

    def spend_mana(self, caster):
        caster.mp = max(0, caster.mp - self.mana_cost)

    def cast(self, caster, target):
        raise NotImplementedError('Each spell must implement cast()')

    def can_cast_on(self, caster, target):
        return self.can_cast(caster) and target is not None and target.is_alive()

    def __str__(self):
        return f'{self.name} : ({self.strength}STR, {self.mana_cost}MP)'

class DamageSpell(Spell):
    """
    Attempts to cast spell on target.

    :returns int | None: Effect damage amount if successful, otherwise None
    """
    def cast(self, caster, target):
        if not self.can_cast_on(caster, target):
            return None

        self.spend_mana(caster)
        damage = self.strength
        modifier = random.uniform(0.9, 1.1)
        final_damage = round(damage * modifier)
        target.take_damage(final_damage)
        return final_damage

    def __str__(self):
        return f'{self.name} (Damage: {self.strength}, Cost: {self.mana_cost}MP)'


class HealSpell(Spell):
    """
    Attempts to cast spell on target.

    :returns int | None: amount healed if successful, otherwise None
    """
    def cast(self, caster, target):
        if not self.can_cast_on(caster, target):
            return None

        self.spend_mana(caster)
        modifier = random.uniform(0.9, 1.1)
        final_amount = round(self.strength * modifier)
        healed = target.restore_health(final_amount)

        return healed

    def __str__(self):
        return f'{self.name} (Heal: {self.strength}, Cost: {self.mana_cost}MP)'

