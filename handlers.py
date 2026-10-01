import questionary
from tracker import (
    create_transaction,
    filter_transactions
)

from database import (
    insert_transaction,
    load_transactions,
    clear_transactions
)


def handle_add(args):
    transaction = create_transaction(args.amount, args.category, args.note)
    insert_transaction(transaction)
    print(
        "Transaction added: "
        f"{transaction.category} — {transaction.amount:_} ₸"
        .replace("_", " ")
    )


def handle_clear(args):
    user_answer = questionary.select(
            "Are you sure you want to clear ALL transactions?",
            choices=['Yes', 'No']
        ).ask()

    if user_answer == 'Yes':
        clear_transactions()
        print("ALL transactions are deleted")


def handle_list(args):
    transactions = load_transactions()
    if not transactions:
        print("No transactions found.")
        return

    transactions = filter_transactions(transactions, args.category, args.from_date, args.to_date)

    for transaction in transactions:
        print(
            f"{transaction.date} || "
            f"{transaction.category} || "
            f"{transaction.amount:_} ||".replace("_", " ") +
            f"{transaction.note if transaction.note else ""}"
        )
