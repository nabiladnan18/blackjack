CARDS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
SUITS = (chr(9829), chr(9830), chr(9824), chr(9827))  # HEARTS, DIAMONDS, SPADES, CLUBS

# CARD GRAPHIC
BASE_CARD = """
     ___ 
    |#  | 
    | # | 
    |__#| 

    """


class Card:
    def __init__(self, card, suit):
        self.card = card
        self.suit = suit

    def __repr__(self) -> str:
        return f"{self.card}{self.suit}"

    def value(self) -> int:
        try:
            card_value = int(self.card)
        except ValueError:
            if self.card != "A":
                return 10
            return 11
        return card_value
