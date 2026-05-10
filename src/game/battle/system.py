"""
Battle System Module

Handles:
- turn flow
- combat actions
- attack/spell resolution
- enemy AI actions
- battle log data generation
- win/loss detection

"""

from enum import Enum, auto
import random
from src.ui import THEME

from src.game.spell import HealSpell


class BattleState(Enum):
    SELECT_MONSTER = auto()
    SELECT_TARGET = auto()
    ENEMY_TURN =auto()
    BATTLE_OVER = auto()

class Turn(Enum):
    PLAYER = 0
    ENEMY = 1

def generate_spell_message(castor, target, spell, amount):
    if isinstance(spell, HealSpell):
        #Heal Spells
        return f'{castor.name} casts {spell.name}! It heals {target.name} {amount} HP.'
    #Damage Spell
    return f'{castor.name} casts {spell.name}! It attacks {target.name}  for {amount} damage.'


class Battle:
    def __init__(self, player1, player2, sfx):
        self.players = [player1, player2]
        self.sfx = sfx
        self.current_turn = Turn.PLAYER
        self.selected_monster = None
        self.selected_spell = None
        self.state = BattleState.SELECT_MONSTER
        self.log = []
        self.max_log_size = 6
        self.winner = None
        self.loser = None

        self.ai_active_monster = None

    def get_monster_side(self, monster):
        if monster in self.players[0]:
            return 'Player'
        elif monster in self.players[1]:
            return 'AI'
        return 'Unknown'

    def generate_attack_message(self, attacker, defender, damage):
        attacker_owner = self.get_monster_side(attacker)

        templates = [
            f'{attacker_owner}\'s {attacker.name} attacks '
            f'{defender.name}! It deals {damage} to {defender.name}!',
            f'{attacker_owner}\'s {attacker.name} strikes '
            f'{defender.name}! It deals {damage} to {defender.name}!'
        ]
        return random.choice(templates)

    def _can_cast_selected_heal_on_ally(self, target_player, target) -> bool:
        return (
            self.state == BattleState.SELECT_TARGET
            and self.selected_monster is not None
            and self.selected_spell is not None
            and isinstance(self.selected_spell, HealSpell)
            and target_player == self.get_current_player()
            and target is not None
            and target.is_alive
        )

    def update(self):
        if self.state == BattleState.ENEMY_TURN:
            self._enemy_turn()

    def _cast_spell_on_target(self, target) -> bool:
        """Check if valid target
        :returns: True if valid, False otherwise"""
        caster = self.selected_monster
        spell = self.selected_spell

        if caster is None or spell is None or target is None:
            return False

        valid_targets = spell.get_valid_targets(
            caster,
            self.players[self.get_current_player()],
            self.players[self.get_opposing_player()],
        )
        if target not in valid_targets:
            return False

        amount = spell.cast(caster, target)

        if amount is None:
            self.add_battle_log(
                f'{caster.name} failed to cast {spell.name}.',
                THEME['battle_log']['PLAYER_LOG_COLOR']
            )
            return False

        self.sfx.play(spell)
        self.add_battle_log(
            generate_spell_message(caster, target, spell, amount),
            THEME['battle_log']['PLAYER_LOG_COLOR'],
            attacker=caster,
            target=target
        )

        if not self.battle_is_over():
            self.end_turn()
        return True

    def try_cast_on_ally(self, target_player, target) -> bool:
        if not self._can_cast_selected_heal_on_ally(target_player, target):
            return False

        return self._cast_spell_on_target(target)

    def resolve_attack(self, attacker, defender) -> int:
        attacker.deplete_energy(1)

        if attacker.energy <= 0:
            attacker.take_damage(attacker.hp)
            self.add_battle_log(
            f'{attacker.name} ran out of energy and collapsed!'
            )
            return 0

        damage = attacker.attack(defender)
        defender.take_damage(damage)
        return damage

    def get_team(self, index):
        """returns a monster list"""
        return self.players[index]

    def add_battle_log(self, message: str, color=None, attacker =None, target=None) -> None:
        self.log.append({
            'text': message,
            'color': color,
            'attacker': attacker,
            'target': target
        })

        if len(self.log) > self.max_log_size:
            self.log.pop(0)

    def battle_is_over(self) -> bool:
        if self.state == BattleState.BATTLE_OVER:
            return True

        player_alive = any(monster.is_alive for monster in self.players[0])
        enemy_alive = any(monster.is_alive for monster in self.players[1])

        if player_alive and enemy_alive:
            return False

        self.state = BattleState.BATTLE_OVER

        if player_alive:
            self.winner, self.loser = 0, 1
            self.add_battle_log(
                f'Player wins!',
                THEME['battle_log']['PLAYER_LOG_COLOR']
            )
        elif enemy_alive:
            self.winner, self.loser = 1, 0
            self.add_battle_log(
                f'AI wins the battle',
                THEME['battle_log']['ENEMY_LOG_COLOR']
            )
        else:
            self.winner, self.loser = None, None
            self.add_battle_log(
                'The battle ends in a draw.'
            )
        return True

    def prepare_enemy_turn(self):
        """Used to add card movement to the enemies choose"""
        enemy_player = self.players[1]
        alive_enemies = [m for m in enemy_player if m.is_alive]

        if not alive_enemies:
            return

        self.ai_active_monster = random.choice(alive_enemies)

    def _enemy_turn(self):
        enemy_player = self.players[1]
        player = self.players[0]

        alive_enemies = [m for m in enemy_player if m.is_alive]
        alive_players = [m for m in player if m.is_alive]

        if not alive_enemies or not alive_players:
            self.state = BattleState.BATTLE_OVER
            return

        attacker = self.ai_active_monster

        if attacker is None or not attacker.is_alive:
            attacker = random.choice(alive_enemies)

        self.ai_active_monster = attacker

        defender = random.choice(alive_players)

        damage = self.resolve_attack(attacker, defender)

        if damage == 0:
            self.add_battle_log(
                f"{attacker.name} is too tired to attack!",
                THEME['battle_log']['ENEMY_LOG_COLOR'],
                attacker=attacker,
                target=defender
            )
        else:
            msg = self.generate_attack_message(attacker, defender, damage)
            self.add_battle_log(
                msg,
                THEME['battle_log']['ENEMY_LOG_COLOR'],
                attacker=attacker,
                target=defender
            )
        self.end_turn()

    def get_current_player(self) -> int:
        """Returns 0 or 1 to correspond with whose turn it is"""
        return self.current_turn.value

    def get_opposing_player(self):
        """Returns index of the AI player"""
        return 1 - self.current_turn.value

    def select_monster(self, player, monster):
        if self.state != BattleState.SELECT_MONSTER:
            return False

        if player != self.get_current_player():
            return False

        if monster is None or not monster.is_alive:
            return False

        #Clicking the selected monster again deselects it
        if self.selected_monster == monster:
            self.cancel_selection()
            return True

        self.selected_monster = monster
        self.selected_spell = None
        self.state = BattleState.SELECT_TARGET

        return True

    def try_attack(self, defender_player, defender):
        if self.state != BattleState.SELECT_TARGET:
            return False

        attacker = self.selected_monster

        if attacker is None or defender is None:
            return False

        if defender_player != self.get_opposing_player():
            return False

        if not attacker.is_alive or not defender.is_alive:
            return False

        if self.selected_spell is not None:
            return self._cast_spell_on_target(defender)

        damage = self.resolve_attack(attacker, defender)

        msg = self.generate_attack_message(attacker, defender, damage)
        self.add_battle_log(
            msg,
            THEME['battle_log']['PLAYER_LOG_COLOR'],
            attacker=attacker,
            target=defender
        )

        self.end_turn()
        return True

    def cancel_selection(self):
        self.selected_monster = None
        self.selected_spell = None
        self.state = BattleState.SELECT_MONSTER

    def end_turn(self):
        self.selected_monster = None
        self.selected_spell = None

        # Change State to enemies
        if self.current_turn == Turn.PLAYER:
            self.current_turn = Turn.ENEMY
            self.state = BattleState.ENEMY_TURN
        # Or player select a monster
        else:
            self.current_turn = Turn.PLAYER
            self.state = BattleState.SELECT_MONSTER
            self.ai_active_monster = None