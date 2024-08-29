import unittest
from random import choice
from unittest.mock import patch

from game import Game
from money import Money
from hand import Hand
from card import Card, SUITS


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.money = Money(5000)
        self.game = Game(self.money.balance)
        self.suit = choice(SUITS)
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.hand = Hand()
        self.bet = 100

    def test_player_wins(self):
        self.player_hand.add_cards([Card("10", self.suit), Card("A", self.suit)])
        self.dealer_hand.add_cards([Card("9", self.suit), Card("8", self.suit)])

        result, winnings = self.game.determine_winner(
            self.player_hand, self.dealer_hand, self.bet
        )
        self.assertEqual(result, "Player wins!")
        self.assertEqual(winnings, 200)

    def test_player_is_blackjack(self):
        self.hand.add_cards([Card("A", self.suit), Card("K", self.suit)])
        self.assertTrue(self.hand.is_blackjack(), True)

    def test_blackjack_tied(self):
        self.player_hand.add_cards([Card("A", self.suit), Card("K", self.suit)])
        self.dealer_hand.add_cards([Card("A", self.suit), Card("J", self.suit)])
        message, winning = self.game.determine_winner(
            self.player_hand, self.dealer_hand, 100
        )

        self.assertEqual(message, "Push: Both player and dealer have Blackjack.")
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

        _, winning = self.game.determine_winner(
            self.player_hand, self.dealer_hand, self.bet
        )
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
        _, winning = self.game.determine_winner(
            self.player_hand, self.dealer_hand, self.bet
        )
        self.assertEqual(winning, 0)

    def test_win_double_down(self):
        self.player_hand.add_cards(
            [Card("10", self.suit), Card("5", self.suit), Card("4", self.suit)]
        )
        self.dealer_hand.add_cards([Card("10", self.suit), Card("8", self.suit)])
        _, winning = self.game.determine_winner(
            self.player_hand, self.dealer_hand, self.bet, doubled_down=True
        )
        self.assertEqual(winning, self.bet * 2 * 2)

    def test_player_wins_insurance(self):
        self.player_hand.add_cards([Card("10", self.suit), Card("A", self.suit)])
        self.dealer_hand.add_cards([Card("A", self.suit), Card("J", self.suit)])

        message, winning = self.game.determine_insurance_payout(self.dealer_hand, 100)

        self.assertEqual(winning, self.bet)
        self.assertEqual(message, "Dealer has Blackjack. Insurance won!")

    def test_player_loses_insurance(self):
        self.dealer_hand.add_cards([Card("A", self.suit), Card("8", self.suit)])
        self.player_hand.add_cards([Card("A", self.suit), Card("10", self.suit)])

        message, winning = self.game.determine_insurance_payout(
            self.dealer_hand, self.bet
        )

        self.assertEqual(winning, 0)
        self.assertEqual(message, "Dealer does not have Blackjack. Insurance is lost.")

    def test_push_insurance(self):
        self.dealer_hand.add_cards([Card("A", self.suit), Card("J", self.suit)])
        self.player_hand.add_cards([Card("A", self.suit), Card("J", self.suit)])

        message, winning = self.game.determine_insurance_payout(
            self.dealer_hand, self.bet
        )

        self.assertEqual(winning, self.bet)
        self.assertEqual(message, "Dealer has Blackjack. Insurance won!")

    def test_double_down_player_bust_loss(self):
        self.dealer_hand.add_cards([Card("A", self.suit), Card("6", self.suit)])
        self.player_hand.add_cards(
            [Card("10", self.suit), Card("5", self.suit), Card("7", self.suit)]
        )

        message, winning = self.game.determine_winner(
            self.player_hand, self.dealer_hand, self.bet, doubled_down=True
        )

        self.assertEqual(winning, 0)
        self.assertEqual(message, "Dealer wins!")

    def test_double_down_dealer_blackjack(self):
        self.dealer_hand.add_cards([Card("A", self.suit), Card("J", self.suit)])
        self.player_hand.add_cards(
            [Card("10", self.suit), Card("5", self.suit), Card("6", self.suit)]
        )

        message, winning = self.game.determine_winner(
            self.player_hand, self.dealer_hand, self.bet, doubled_down=True
        )

        self.assertEqual(winning, 0)
        self.assertEqual(message, "Dealer wins with Blackjack.")

    def test_player_wins_blackjack(self):
        self.dealer_hand.add_cards([Card("A", self.suit), Card("10", self.suit)])
        self.player_hand.add_cards([Card("A", self.suit), Card("J", self.suit)])

        message, winnings = self.game.determine_winner(
            self.player_hand, self.dealer_hand, self.bet
        )

        self.assertEqual(message, f"Player wins with Blackjack! Payout: ${winnings}")
        self.assertEqual(winnings, int(self.bet * 2.5))

    # @patch("builtins.input", return_values=50)
    def test_prompt_insurance_bet(self):
        self.dealer_hand.add_cards([Card("A", self.suit), Card("10", self.suit)])
        self.player_hand.add_cards([Card("10", self.suit), Card("7", self.suit)])

        with patch("builtins.input", return_value=int(self.bet / 4)):
            insurance_bet = self.game.insurance_bet_prompt(self.bet)

        self.assertEqual(insurance_bet, int(self.bet / 4))


class TestMockUserInput(unittest.TestCase):
    def setUp(self):
        # Initializing the game with a starting balance of 5000
        self.money = Money(5000)
        self.game = Game(self.money.balance)
        self.suit = choice(SUITS)
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.bet = 100

    @patch("builtins.input", side_effect=["0", "h", "s"])
    # side_effect --> mocking user's input
    def test_no_insurance_player_wins(self, mock_input):
        # Set up the controlled deck
        self.game.deck = [
            Card("8", self.suit),  # Dealer
            Card("10", self.suit),  # Player
            Card("8", self.suit),  # Dealer
            Card("3", self.suit),  # Player
            Card("A", self.suit),  # Dealer
            Card("8", self.suit),  # Player
        ]

        winnings = self.game.play(100)

        # Expected state:
        # Player: 8, 3, 10 (21)
        # Dealer: A, 8, 8 (17)
        # Player loses insurance

        self.assertEqual((self.money.balance + self.bet * 2 - 50), 5150)
        # Initial money + bet + bet - insurance

        self.assertEqual(winnings, 200)  # Player --> 21

    @patch(
        "builtins.input", side_effect=["50", "h", "s"]
    )  # insurance bet 50, hit, then stand
    def test_player_decision_flow(self, mock_input):
        # Mock the deck to control the card draws
        self.game.deck = [
            Card("10", self.suit),  # player
            Card("J", self.suit),  # dealer
            Card("8", self.suit),  # player
            Card("A", self.suit),  # dealer
            Card("3", self.suit),  # player
        ]

        winnings = self.game.play(100)

        # Expected state:
        # Player: 3, 8, 10 (21)
        # Dealer: A, J (21)
        # Dealer wins with BlackJack
        # Player wins insurance 2:1

        self.assertEqual((self.money.balance - self.bet + 50 * 2), self.money.balance)
        # * Initial money - lost bet of 100 + (insurance bet 50 + dealer matches 50)

        self.assertEqual(winnings, 0)  # Dealer --> BlackJack

    @patch("builtins.input", side_effect=["d"])
    def test_double_down(self, mock_input):
        self.game.deck = [
            Card("10", self.suit),
            Card("5", self.suit),
            Card("7", self.suit),  # dealer
            Card("10", self.suit),  # player
            Card("5", self.suit),  # dealer
            Card("8", self.suit),  # player
        ]

        # Expected state:
        # Player: 8, 10, 5
        # Dealer: 5, doesn't really matter
        # Player bust --> dealer wins

        winnings = self.game.play(100)

        self.assertEqual(winnings, 0)

    @patch("builtins.input", side_effect=["s"])
    def test_player_wins_with_blackjack(self, mock_input):
        self.game.deck = [
            Card("10", self.suit),
            Card("A", self.suit),
            Card("10", self.suit),  # dealer
            Card("J", self.suit),  # player
            Card("10", self.suit),  # dealer
            Card("A", self.suit),  # player
        ]

        # Expected state:
        # Player: 8, 10, 5
        # Dealer: A, 10, A
        # Player wins with Blackjack

        winnings = self.game.play(100)

        self.assertEqual(winnings, 250)


#! Really gotta learn to use pytest library
# * seems less verbose and the use of fixture and mark.parameterize sounds noice!
