from dataclasses import dataclass

@dataclass
class Transaction:
    id: str
    date: str
    amount: int
    category: str
    note:str | None = None