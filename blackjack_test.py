import unittest
from random import choice

from game import Game
from money import Money
from hand import Hand
from card import Card, SUITS


class TestBlackJack(unittest.TestCase):
    def setUp(self):
        self.money = Money(5000)
        self.game = Game(self.money.balance)
        self.suit = choice(SUITS)
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.hand = Hand()

    def test_player_wins(self):
        self.player_hand.add_cards([Card("10", self.suit), Card("A", self.suit)])
        self.dealer_hand.add_cards([Card("9", self.suit), Card("8", self.suit)])

        result, winnings = self.game.determine_winner(
            self.player_hand, self.dealer_hand, 100
        )
        self.assertEqual(result, "Player wins!")
        self.assertEqual(winnings, 200)

    def test_player_is_blackjack(self):
        self.hand.add_cards([Card("A", self.suit), Card("K", self.suit)])
        self.assertTrue(self.hand.is_blackjack(), True)

    def test_blackjack_tied(self):
        self.player_hand.add_cards([Card("A", self.suit), Card("K", self.suit)])
        self.dealer_hand.add_cards([Card("A", self.suit), Card("J", self.suit)])
        _, winning = self.game.determine_winner(self.player_hand, self.dealer_hand, 100)
        self.assertEqual(winning, 0)

    def test_hand_is_bust(self):
        hand = Hand()
        hand.add_cards(
            [
                Card("10", self.suit),
                Card("10", self.suit),
                Card("2", self.suit),
            ]
        )
        self.assertEqual(hand.is_bust(), True)

    def test_tie_both_blackjack(self):
        self.player_hand.add_cards([Card("A", self.suit), Card("K", self.suit)])
        self.dealer_hand.add_cards([Card("A", self.suit), Card("J", self.suit)])

        _, winning = self.game.determine_winner(self.player_hand, self.dealer_hand, 100)
        self.assertEqual(winning, 0)

    def test_player_wins_regular_hand(self):
        self.player_hand.add_card(Card("5", self.suit))
        self.player_hand.add_card(Card("10", self.suit))
        self.dealer_hand.add_card(Card("6", self.suit))
        self.dealer_hand.add_card(Card("7", self.suit))
        self.player_hand.add_card(Card("5", self.suit))
        self.dealer_hand.add_card(Card("6", self.suit))

        _, winning = self.game.determine_winner(self.player_hand, self.dealer_hand, 100)
        self.assertEqual(winning, 200)

    def test_player_loses_regular_hand(self):
        self.player_hand.add_cards(
            [Card("10", self.suit), Card("5", self.suit), Card("4", self.suit)]
        )
        self.dealer_hand.add_cards([Card("10", self.suit), Card("10", self.suit)])
        _, winning = self.game.determine_winner(self.player_hand, self.dealer_hand, 100)
        self.assertEqual(winning, 0)

    def test_win_double_down(self):
        self.player_hand.add_cards(
            [Card("10", self.suit), Card("5", self.suit), Card("4", self.suit)]
        )
        self.dealer_hand.add_cards([Card("10", self.suit), Card("8", self.suit)])
        _, winning = self.game.determine_winner(
            self.player_hand, self.dealer_hand, 100, doubled_down=True
        )
        self.assertEqual(winning, 400)

    def test_player_wins_insurance(self):
        self.player_hand.add_cards([Card("10", self.suit), Card("A", self.suit)])
        self.dealer_hand.add_cards([Card("A", self.suit), Card("J", self.suit)])

        _, winning = self.game.determine_insurance_payout(self.dealer_hand, 100)

        self.assertEqual(winning, 100)

    def test_player_loses_insurance(self):
        self.dealer_hand.add_cards([Card("A", self.suit), Card("8", self.suit)])
        self.player_hand.add_cards([Card("A", self.suit), Card("10", self.suit)])

        _, winning = self.game.determine_insurance_payout(self.player_hand, 100)

        self.assertEqual(winning, 0)

    def test_push_insurance(self):
        self.dealer_hand.add_cards([Card("A", self.suit), Card("J", self.suit)])
        self.player_hand.add_cards([Card("A", self.suit), Card("J", self.suit)])

        _, winning = self.game.determine_insurance_payout(self.player_hand, 100)

        self.assertEqual(winning, 100)


#! Really gotta learn to use pytest library
# * seems less verbose and the use of fixture and mark.parameterize sounds noice!
