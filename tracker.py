import json
import uuid
from datetime import datetime
from pathlib import Path
from models import Transaction
from dataclasses import asdict

DATA_FILE = Path(__file__).resolve().parent / 'transactions.json'

def load_transactions():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            transactions = json.load(file)
            return [Transaction(**transaction) for transaction in transactions]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError("Invalid json file") from error

def save_transactions(transactions):
    data = [asdict(transaction) for transaction in transactions]

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

### ADD
def add_transaction(transactions, amount, category, note=None):
    # Category validation
    if not isinstance(category, str):
        raise ValueError("Category must be a string")

    category = category.strip().lower()

    if not category:
        raise ValueError("Invalid category")

    # Amount validation
    if type(amount) is not int or amount <= 0:
        raise ValueError("Invalid amount")

    transaction = Transaction(
        id=str(uuid.uuid4()),
        date=datetime.now().isoformat(timespec="seconds"),
        amount=amount,
        category=category,
        note=note
    )
    transactions.append(transaction)
    return transaction

### FIND TRANSACTIONS
def find_transactions(transactions: list, category:str) -> list:
    category = category.strip().lower()
    if not category:
        raise ValueError("Category cannot be empty")

    matches = [transaction for transaction in transactions if transaction.category.strip().lower() == category]
    if not matches:
        raise ValueError(
            f"No transactions with category '{category}' exist"
        )

    return matches

### FILTER TRANSACTIONS

def filter_transactions(
    transactions: list,
    category: str = None,
    from_date=None,
    to_date=None,
) -> list:

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

### DELETE
def delete_transaction(transactions, trans_id):
    for transaction in transactions:
        if transaction.id == trans_id:
            transactions.remove(transaction)
            return transaction

    raise ValueError(f"Transaction with id {trans_id} does not exist")

### SUMMARIZE
def summarize_by_category(transactions):
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

def calculate_total(transactions):
    return sum(transaction.amount for transaction in transactions)