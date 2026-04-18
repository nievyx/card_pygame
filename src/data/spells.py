from src.game.spell import DamageSpell, HealSpell

fireball = DamageSpell(name='Fireball',
                       strength=12,
                       mana_cost=5,
                       icon='src/assets/icons/fire_spell_2.png')

fire_blast = DamageSpell(name='Fireblast',
                       strength=fireball.strength+3,
                       mana_cost=fireball.mana_cost+5,
                       icon='src/assets/icons/fire_spell_1.png')


ice_bolt = DamageSpell(name='Icebolt',
                      strength=18,
                      mana_cost=6,
                      icon='src/assets/icons/ice_spell_1.png')

ice_shards = DamageSpell(name='Ice Shards',
                      strength=ice_bolt.strength+3,
                      mana_cost=ice_bolt.mana_cost+3,
                      icon='src/assets/icons/ice_spell_2.png')

ice_storm = DamageSpell(name='Ice Storm',
                      strength=ice_shards.strength+3,
                      mana_cost=ice_shards.mana_cost+3,
                      icon='src/assets/icons/ice_spell_3.png')

vine_attack = DamageSpell(name='Vine Attack',
                       strength=12,
                       mana_cost=5,
                       icon='src/assets/icons/earth_spell_1.png')

light_heal = HealSpell(name='Light Heal',
                       strength=15,
                       mana_cost=6,
                       icon='src/assets/icons/heal_spell_1.png',
                       use_in_overworld=True)

mid_heal = HealSpell(name='Mid Heal',
                       strength=light_heal.strength+3,
                       mana_cost=light_heal.mana_cost+3,
                       icon='src/assets/icons/heal_spell_2.png',
                       use_in_overworld=True)

strong_heal = HealSpell(name='Strong Heal',
                       strength=mid_heal.strength+3,
                       mana_cost=mid_heal.mana_cost+3,
                       icon='src/assets/icons/heal_spell_3.png',
                       use_in_overworld=True)
