from src.game.spell import DamageSpell, HealSpell

fireball = DamageSpell(name='Fireball',
                       strength=12,
                       mana_cost=5,
                       icon='🔥')

ice_bolt = DamageSpell(name='Icebolt',
                      strength=18,
                      mana_cost=6,
                      icon='❄')

light_heal = HealSpell(name='Light Heal',
                       strength=15,
                       mana_cost=8,
                       use_in_overworld=True)