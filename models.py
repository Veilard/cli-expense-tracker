from dataclasses import dataclass
from exceptions import InvalidAmountError, InvalidCategoryError


@dataclass
class Transaction:
    id: str
    date: str
    amount: int
    category: str
    note:str | None = None


    def __post_init__(self) -> None:
        if type(self.amount) is not int or self.amount <= 0:
            raise InvalidAmountError("Invalid amount")

        if not isinstance(self.category, str):
            raise InvalidCategoryError("Category must be a string")

        self.category = self.category.strip().lower()

        if not self.category:
            raise InvalidCategoryError("Invalid category")


    @property
    def formatted_amount(self) -> str:
        return f"{self.amount:_} ₸".replace("_", " ")


class ExpenseTracker:
    def __init__(self) -> None:
        self.transactions: list[Transaction] = []

    def add(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def calc_total(self) -> int:
        return sum(x.amount for x in self.transactions)