from dataclasses import dataclass

@dataclass
class Transaction:
    id: str
    date: str
    amount: int
    category: str
    note:str | None = None

class ExpenseTracker:
    def __init__(self):
        self.transactions = []

    def add(self, transaction):
        self.transactions.append(transaction)

    def calc_total(self):
        return sum(x.amount for x in self.transactions)