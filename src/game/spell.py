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
        return getattr(caster, 'mp', 0) >= self.mana_cost and caster.use_in_overworld

    def spend_mana(self, caster):
        caster.mp = max(0, caster.mp - self.mana_cost)

    def cast(self, castor, target):
        raise NotImplementedError('Each spell must implement cast()')

    def __str__(self):
        return f'{self.name} ({self.strength})'


class DamageSpell(Spell):
    def cast(self, castor, target):


        damage = self.strength
        modifier = random.uniform(0.9, 1.1)
        final_damage = round(damage * modifier)
        target.take_damage(final_damage)
        return final_damage

    def __str__(self):
        return f'{self.name} (Base Damage: {self.strength})'


class HealSpell(Spell):
    # TODO: Heal spells will currently only heal castor
    # TODO: Also target refers to the enemy, when it should refer to the healed (Changed target name to castor name)
    def cast(self, caster, target):
        final_amount = self.strength
        print(f'{caster.name} casts {self.name} on {caster.name}. {final_amount} points healed.')
        caster.restore_health(final_amount)
        return final_amount


# These have no use now
def get_spell_type(spell):
    return spell.__class__.__name__


def check_spells(spell_list, *spell_types):
    return [spell for spell in spell_list if isinstance(spell, spell_types)]

