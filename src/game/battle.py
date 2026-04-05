from enum import Enum, auto

class BattleState(Enum):
    SELECT_MONSTER = auto()
    SELECT_TARGET = auto()
    ENEMY_TURN =auto()
    BATTLE_OVER = auto()

class Battle:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_turn = 0
        self.selected_monster = None
        self.state = BattleState.SELECT_MONSTER


    def get_current_player(self):
         return self.current_turn

    def get_opposing_player(self):
        return 1 - self.current_turn

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
        self.current_turn = self.get_opposing_player()

    def pass_ai_turn(self):
        if self.current_turn != 1:
            return False

        self.end_turn()
        return True


    # Old below

    def try_attack_clicked_away(self, defender):
        attacker = self.selected_monster

        if attacker is None or defender is None:
            return

        if not attacker.is_alive() or not defender.is_alive():
            return

        defender.take_damage(attacker.strength)







