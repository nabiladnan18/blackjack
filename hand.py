from card import Card

BLACKJACK = "BLACKJACK"
GOAL = 21


class Hand:
    def __init__(self):
        self.cards: list[Card] = []

    def __repr__(self) -> str:
        return ", ".join(str(card) for card in self.cards)

    def add_card(self, card):
        self.cards.append(card)

    def add_cards(self, cards: list):
        self.cards.extend(cards)

    def value(self):
        aces = 0
        total = 0
        cards: list[Card] = self.cards
        cards = cards.copy()
        for card in cards:
            value = card.value()
            if card.card == "A":
                aces += 1
            total += value
        while total > GOAL and aces:
            total -= 10
            aces -= 1
        return total

    def is_blackjack(self):
        if len(self.cards) == 2:
            aces = any(card.card == "A" for card in self.cards)
            faces = any(card.card in ("J", "Q", "K") for card in self.cards)
            return aces and faces
        return False

    def is_bust(self):
        return self.value() > GOAL
