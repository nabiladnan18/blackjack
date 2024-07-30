class Money:
    def __init__(self, money: int):
        self.balance = money

    def win(self, sum: int):
        self.balance += sum

    def bet(self, amount):
        if amount > self.balance:
            raise ValueError("Cannot bet more than balance!")
        self.balance -= amount

    def __repr__(self) -> str:
        return f"${self.balance}"
