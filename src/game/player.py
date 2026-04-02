class Player:
    def __init__(self, name: str) -> None:
        self.name = name

        # All owned monsters
        self.roster = [] # Cards owned and collected by the player

        # Per-Match
        self.deck = [] # Being played in battlefield
        self.hand = [] # In players hand, visible to player
        self.board = [] # TODO : do u need this is v yugioh
        self.discard = []
        self.graveyard = [] # List of cards defeated

        # Player Stats
        self.gold = 0
        # TODO : deside if player has health

class OwnedMonster:
    def __init__(self, monster) -> None:
        self.monster = monster
        self.level = 1
        self.nickname = None

        # Note: Players deck be will pre-shuffled before a card is drawn, do not worry about getting a random card
        def draw_card(self):
            """ draw a card from the deck
            Works by checking if card in deck not empty, then subsequently adding to hand and removing from deck """
            if self.deck:
                self.hand.append(self.deck.pop())

        def kill_monster(self, monster):
            if monster in self.board: #TODO: this is if cards need to be played on board and not just attack hand
                self.board.remove(monster)
                self.graveyard.append(monster)
                #TODO: this belong here

