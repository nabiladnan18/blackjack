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

    def test_player_wins(self):
        player_hand = Hand()
        player_hand.add_cards([Card("10", choice(SUITS)), Card("A", choice(SUITS))])

        dealer_hand = Hand()
        dealer_hand.add_cards([Card("9", choice(SUITS)), Card("8", choice(SUITS))])

        result, winnings = self.game.determine_winner(player_hand, dealer_hand, 100)
        self.assertEqual(result, "Player wins!")
        self.assertEqual(winnings, 200)

    def test_player_is_blackjack(self):
        hand = Hand()
        hand.add_cards([Card("A", choice(SUITS)), Card("K", choice(SUITS))])
        self.assertTrue(hand.is_blackjack(), True)

    def test_blackjack_tied(self):
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_cards([Card("A", choice(SUITS)), Card("K", choice(SUITS))])
        dealer_hand.add_cards([Card("A", choice(SUITS)), Card("J", choice(SUITS))])
        _, winning = self.game.determine_winner(player_hand, dealer_hand, 100)
        self.assertEqual(winning, 0)

    def test_hand_is_bust(self):
        hand = Hand()
        hand.add_cards(
            [
                Card("10", choice(SUITS)),
                Card("10", choice(SUITS)),
                Card("2", choice(SUITS)),
            ]
        )
        self.assertEqual(hand.is_bust(), True)

    # def test_player_blackjack_win(self):


#! Really gotta learn to use pytest library
# * seems less verbose and the use of fixture and mark.parameterize sounds noice!
# import pytest
# from .blackjack import Hand

# # @pytest.fixture
# ...
#
# @pytest.mark.parametrize(
#     "hand",
#     "value()",
#     [
#         (Hand(["A", "8"]), 19),
#         (Hand(["A", "J"]), "BLACKJACK"),
#         (Hand(["A", "10"]), 21),
#         (Hand(["2", "7"]), 9),
#     ],
# )
# def test_dealt_hand_values(hand, value):
#     assert hand.value() == value

# @pytest.mark.parametrize(
#     "num1, num2, expected", [(3, 2, 5), (4, 10, 14), (100, -1, 99)]
# )
# def test_add(num1, num2, expected):
#     assert add(num1, num2) == expected
