from src.config import PLAYER_LOG_COLOR, ENEMY_LOG_COLOR
from enum import Enum, auto
import random

class BattleState(Enum):
    SELECT_MONSTER = auto()
    SELECT_TARGET = auto()
    ENEMY_TURN =auto()
    BATTLE_OVER = auto()

class Turn(Enum):
    PLAYER = 0
    ENEMY = 1

class Battle:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_turn = Turn.PLAYER
        self.selected_monster = None
        self.state = BattleState.SELECT_MONSTER
        self.log = []
        self.max_log_size = 6

    def update(self):
        if self.state == BattleState.ENEMY_TURN:
            self._enemy_turn()

    def add_battle_log(self, message: str, color=None) -> None:
        self.log.append({
            'text': message,
            'color': color
        })

        if len(self.log) > self.max_log_size:
            self.log.pop(0)

        print(self.log) #TODO: DEBUG

    def generate_attack_message(self, attacker, defender, damage):
        templates = [
            f'{attacker.name} attacks {defender.name}! It deals {damage} to {defender.name}!',
        ]
        return random.choice(templates)

    def _enemy_turn(self):
        enemy_player = self.players[1]
        player = self.players[0]

        alive_enemies = [m for m in enemy_player if m.is_alive()]
        alive_players = [m for m in player if m.is_alive()]

        if not alive_enemies or not alive_players:
            self.state = BattleState.BATTLE_OVER
            return

        attacker = random.choice(alive_enemies)
        defender = random.choice(alive_players)

        defender.take_damage(attacker.strength)

        msg = self.generate_attack_message(attacker, defender, attacker.strength)
        self.add_battle_log(msg, ENEMY_LOG_COLOR)

        self.end_turn()

    def get_current_player(self) -> int:
        """Returns 0 or 1 to correspond with whose turn it is"""
        return self.current_turn.value

    def get_opposing_player(self):
        return 1 - self.current_turn.value

    def select_monster(self, player, monster):
        if self.state != BattleState.SELECT_MONSTER:
            return False

        if player != self.get_current_player():
            return False

        if monster is None or not monster.is_alive():
            return False

        self.selected_monster = monster
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

        if not attacker.is_alive() or not defender.is_alive():
            return False

        defender.take_damage(attacker.strength)

        msg = self.generate_attack_message(attacker, defender, attacker.strength)
        self.add_battle_log(msg, PLAYER_LOG_COLOR)

        self.end_turn()
        return True

    def end_turn(self):
        self.selected_monster = None

        # Change State to enemies
        if self.current_turn == Turn.PLAYER:
            self.current_turn = Turn.ENEMY
            self.state = BattleState.ENEMY_TURN
        # Or player select a monster
        else:
            self.current_turn = Turn.PLAYER
            self.state = BattleState.SELECT_MONSTER