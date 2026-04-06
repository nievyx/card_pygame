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

    def update(self):
        if self.state == BattleState.ENEMY_TURN:
            self._enemy_turn()

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

        print(f'{attacker.name} attacks {defender.name}!')

        self.end_turn()



    def get_current_player(self):
         return self.current_turn

    def get_opposing_player(self):
        return Turn.ENEMY if self.current_turn == Turn.PLAYER else Turn.PLAYER

    def select_monster(self, player, monster):
        if player != self.get_current_player():
            return False

        if monster is None or not monster.is_alive():
            return False

        self.selected_monster = monster
        return True

    def try_attack(self, defender_player, defender):
        attacker = self.selected_monster

        if attacker is None or defender is None:
            return False

        if defender_player != self.get_opposing_player():
            return False

        if not attacker.is_alive() or not defender.is_alive():
            return False

        defender.take_damage(attacker.strength)
        self.end_turn()
        return True

    def end_turn(self):
        self.selected_monster = None

        # Switch turn to enemy
        self.current_turn = self.get_opposing_player()

        # Change State to enemies
        if self.current_turn == Turn.ENEMY:
            self.state = BattleState.ENEMY_TURN
        # Or player select a monster
        else:
            self.state = BattleState.SELECT_MONSTER

    def pass_ai_turn(self):
        if self.current_turn != 1:
            return False

        self.end_turn()
        return True




