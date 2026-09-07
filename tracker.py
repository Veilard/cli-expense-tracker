import json
import uuid
from datetime import datetime
from pathlib import Path

path = f"{Path.cwd()}\\transactions.json"

def load_transactions():
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.decoder.JSONDecodeError as error:
        raise ValueError("Invalid json file") from error

def add_transaction(transactions, amount, category, note=None):
    transaction = {
        "id" : str(uuid.uuid4()),
        "date" : datetime.now().replace(microsecond=0),
        "amount" : amount,
        "category" : category,
        "note" : note
    }

    if amount < 0:
        raise ValueError("Invalid amount")
    else:
        transactions.append(transaction)

def save_transactions(transactions):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            transactions,
            file,
            ensure_ascii=False,
            indent=2,
            default=str,
        )
