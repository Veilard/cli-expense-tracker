import json
import uuid
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / 'transactions.json'

def load_transactions():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError("Invalid json file") from error

def save_transactions(transactions):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            transactions,
            file,
            ensure_ascii=False,
            indent=2,
            default=str,
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

    transaction = {
        "id" : str(uuid.uuid4()),
        "date" : datetime.now().replace(microsecond=0),
        "amount" : amount,
        "category" : category,
        "note" : note
    }

    transactions.append(transaction)
    return transaction

### DELETE
def delete_transaction(transactions: list, category: str) -> dict:
    category = category.strip().lower()
    if not category:
        raise ValueError("Category cannot be empty")

    matches = [transaction for transaction in transactions if transaction["category"] == category]
    if not matches:
        f"No transactions with category '{category}' exists"

    transactions.remove(removed_transaction)
    return removed_transaction

### SUMMARIZE
def summarize_by_category(transactions):
    totals_by_category = {}

    for transaction in transactions:
        category = transaction["category"].strip().lower()
        totals_by_category[category] = (
            totals_by_category.get(category, 0)
            + transaction["amount"]
        )

    return dict(
        sorted(
            totals_by_category.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )

def calculate_total(transactions):
    return sum(transaction["amount"] for transaction in transactions)