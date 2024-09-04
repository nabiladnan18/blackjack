import random
from card import Card, CARDS, SUITS
from hand import Hand
from money import Money


class Game:
    def __init__(self, buy_in: int) -> None:
        self.money = Money(buy_in)
        self.deck = self.create_deck()

    def create_deck(self):
        # 4 decks to draw from
        deck = [
            Card(card, suit) for card in CARDS for suit in SUITS for _ in range(0, 4)
        ]
        random.shuffle(deck)
        return deck

    def deal_card(self):
        return self.deck.pop()

    def insurance_bet_prompt(self, bet: int):
        insurance_bet = int(
            input(
                "Dealer has a good chance of getting a Blackjack. You may choose to place an insurance bet. You will lose the insurance if the dealer does not have Blackjack. If the dealer has Blackjack, the insurance will be returned. You may also choose not to place an insurance bet. In that case, enter 0. How much insurance bet would you like to place?: "
            )
        )
        if insurance_bet > 0.5 * bet:
            return "Insurance bet must be below half of your bet."
        return insurance_bet

    def determine_insurance_payout(self, dealer_hand: Hand, insurance_bet: int):
        if dealer_hand.is_blackjack():
            self.money.win(insurance_bet * 2)
            return "Dealer has Blackjack. Insurance won!", insurance_bet
        return "Dealer does not have Blackjack. Insurance is lost.", 0

    def determine_winner(
        self,
        player_hand: Hand,
        dealer_hand: Hand,
        bet: int,
        doubled_down=False,
    ):
        # Check for Blackjack
        if player_hand.is_blackjack() and dealer_hand.is_blackjack():
            self.money.win(bet)  # Return bet
            return "Push: Both player and dealer have Blackjack.", 0
        elif player_hand.is_blackjack():
            winnings = int(bet * 2.5)  # 3:2 payout
            self.money.win(winnings)
            return "Player wins with Blackjack!", winnings
        elif dealer_hand.is_blackjack():
            return "Dealer wins with Blackjack.", 0

        # Standard winning conditions
        if player_hand.is_bust():
            return "Dealer wins!", 0
        if dealer_hand.is_bust() or player_hand.value() > dealer_hand.value():
            winnings = bet * 2
            if doubled_down:
                winnings *= 2
            self.money.win(winnings)
            return "Player wins!", winnings
        if player_hand.value() == dealer_hand.value():
            return "Push", 0

        return "Dealer wins!", 0

    def play(self, current_balance, bet):
        player_hand = Hand()
        dealer_hand = Hand()
        doubled_down = False
        first_move = True
        move = None
        insurance_bet_placed = False

        for _ in range(0, 2):
            player_hand.add_card(self.deal_card())
            dealer_hand.add_card(self.deal_card())

        while not player_hand.is_bust():
            print("Dealer: ???")
            print(f"Dealer: *** {dealer_hand.cards[0]}\n")
            # show cards here
            print(f"Player: {player_hand.value()}")
            print(f"Player: {player_hand}")

            if first_move:
                if player_hand.is_blackjack():
                    break
                if dealer_hand.cards[0].card == "A":
                    while True:
                        insurance_bet_placed = self.insurance_bet_prompt(bet)
                        try:
                            int(insurance_bet_placed)
                        except ValueError:
                            print(
                                "You must enter an integer value to place your bet. Enter 0 if you do not wish to place an insurance bet."
                            )
                        break
                if current_balance <= bet * 2:
                    move = input("(H)it, (S)tand or (D)ouble Down?: ").lower()
            else:
                move = input("(H)it or (S)tand?: ").lower()

            if move == "h":
                player_hand.add_card(self.deal_card())
                first_move = False
            elif move == "s":
                break
            elif move == "d" and first_move:
                doubled_down = True
                self.money.bet(bet)
                bet *= 2
                player_hand.add_card(self.deal_card())
                break
            else:
                print("\nInvalid move; please choose again.")

        while dealer_hand.value() <= 17:
            dealer_hand.add_card(self.deal_card())

        if insurance_bet_placed:
            message, winning = self.determine_insurance_payout(
                dealer_hand, insurance_bet_placed
            )
            print(message)

            self.money.win(winning)

        result, winnings = self.determine_winner(
            player_hand, dealer_hand, bet, doubled_down
        )

        if not player_hand.is_bust() or winnings > 0:
            print(f"Dealer: {dealer_hand.value()}")
            print(f"Dealer: {dealer_hand.__repr__()}\n")

        print(f"Player: {player_hand.value()}")
        print(f"Player: {player_hand.__repr__()}\n")
        print(result)

        return winnings
