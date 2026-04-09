from src.game.spell import DamageSpell, HealSpell

fireball = DamageSpell(name='Fireball',
                       strength=30,
                       mana_cost=10,
                       icon='🔥')

icebolt = DamageSpell(name='Icebolt',
                      strength=40,
                      mana_cost=10,
                      icon='❄')

light_heal = HealSpell(name='Light Heal',
                       strength=15,
                       mana_cost=8,
                       use_in_overworld=True)