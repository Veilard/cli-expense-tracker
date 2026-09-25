import uuid
from datetime import datetime
from models import Transaction
from exceptions import TransactionNotFoundError


def create_transaction(
        amount: int,
        category: str,
        note: str | None = None
) -> Transaction:
    transaction = Transaction(
        id=str(uuid.uuid4()),
        date=datetime.now().isoformat(timespec="seconds"),
        amount=amount,
        category=category,
        note=note
    )
    return transaction


def find_transactions(
        transactions: list[Transaction],
        category: str
) -> list[Transaction]:
    category = category.strip().lower()
    if not category:
        raise ValueError("Category cannot be empty")

    matches = [transaction for transaction in transactions if transaction.category.strip().lower() == category]
    if not matches:
        raise TransactionNotFoundError(
            f"No transactions with category '{category}' exist"
        )

    return matches


def filter_transactions(
        transactions: list[Transaction],
        category: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
) -> list[Transaction]:
    if category:
        category = category.strip().lower()

        transactions = [
            transaction
            for transaction in transactions
            if transaction.category.strip().lower() == category
        ]

    if from_date:
        from_date = datetime.strptime(from_date, "%Y-%m-%d").date()

        transactions = [
            transaction
            for transaction in transactions
            if datetime.fromisoformat(transaction.date).date() >= from_date
        ]

    if to_date:
        to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

        transactions = [
            transaction
            for transaction in transactions
            if datetime.fromisoformat(transaction.date).date() <= to_date
        ]

    return transactions


def summarize_by_category(transactions: list[Transaction]) -> dict[str, int]:
    totals_by_category = {}

    for transaction in transactions:
        category = transaction.category.strip().lower()
        totals_by_category[category] = (
                totals_by_category.get(category, 0)
                + transaction.amount
        )

    return dict(
        sorted(
            totals_by_category.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )


def calculate_total(transactions: list[Transaction]) -> int:
    return sum(transaction.amount for transaction in transactions)
