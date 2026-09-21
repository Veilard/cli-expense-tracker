from dataclasses import dataclass
from exceptions import InvalidAmountError, InvalidCategoryError

@dataclass
class Transaction:
    id: str
    date: str
    amount: int
    category: str
    note:str | None = None


    def __post_init__(self):
        if type(self.amount) is not int or self.amount <= 0:
            raise InvalidAmountError("Invalid amount")

        if not isinstance(self.category, str):
            raise InvalidCategoryError("Category must be a string")

        self.category = self.category.strip().lower()

        if not self.category:
            raise InvalidCategoryError("Invalid category")


    @property
    def formatted_amount(self):
        return f"{self.amount:_} ₸".replace("_", " ")


class ExpenseTracker:
    def __init__(self):
        self.transactions = []

    def add(self, transaction):
        self.transactions.append(transaction)

    def calc_total(self):
        return sum(x.amount for x in self.transactions)