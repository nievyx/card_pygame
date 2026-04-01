class Player:
    def __init__(self, name: str) -> None:
        self.name = name

        # All owned monsters
        self.roster = []

        # Per-Match
        self.deck = []
        self.hand = []
        self.board = []
        self.discard = []

        # Player Stats
        self.gold = 0
        # TODO : deside if player has health

        # Note: Players deck be will pre-shuffled before a card is drawn, do not worry about getting a random card
        def draw_card(self):
            pass