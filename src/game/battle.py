class Battle:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_turn = 0
        self.selected_monster = None

    def select_monster(self, monster):
        pass

    def try_attack_clicked_away(self, defender):
        attacker = self.selected_monster

        if attacker is None or defender is None:
            return

        if not attacker.is_alive() or not defender.is_alive():
            return

        defender.take_damage(attacker.strength)





