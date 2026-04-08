import random

class Spell:
    def __init__(self,
                 name: str,
                 spell_type: str,
                 strength: int,
                 mana_cost: int,
                 icon='',
                 use_in_overworld: bool = False
                 ):
        self.name = name
        self.type = spell_type
        self.strength = strength
        self.mana_cost = mana_cost
        self.icon = icon
        self.use_in_overworld = use_in_overworld

    def __str__(self):
        return f'{self.name} ({self.strength})'

    def cast(self, castor, target):
        raise NotImplementedError('Each spell must implement cast()')


class DamageSpell(Spell):
    def cast(self, castor, target):
        damage = round(int(self.strength) + (int(castor.intelligence) / 3))
        modifier = random.uniform(0.9, 1.1)
        final_damage = round(damage * modifier)
        print(f'{castor.name} casts {self.name} {self.icon} on {target.name} it dealt {final_damage} damage!') #TODO: this is debug only

        # Apply damage and check for fainting
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

#TODO: remove these after connecting new data/spells.py
fireball = DamageSpell(name='Fireball',
                       spell_type='damage',
                       strength=30,
                       mana_cost=10,
                       icon='🔥')


icebolt = DamageSpell(name='Icebolt',
                      spell_type='damage',
                      strength=40,
                      mana_cost=10,
                      icon='❄')

light_heal = HealSpell(name='Light Heal',
                       spell_type='heal',
                       strength=15,
                       mana_cost=8,
                       use_in_overworld=True)