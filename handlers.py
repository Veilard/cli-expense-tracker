from datetime import datetime

import questionary

from questionary import Choice

from tracker import (
    create_transaction,
    filter_transactions,
    find_transactions,
    summarize_by_category,
    calculate_total
)

from database import (
    insert_transaction,
    load_transactions,
    clear_transactions,
    delete_transaction as delete_transaction_db,
    replace_transaction
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

    args.from_date = datetime.strptime(args.from_date or None, "%Y-%m-%d").date() if args.from_date else None
    args.to_date = datetime.strptime(args.to_date, "%Y-%m-%d").date() if args.to_date else None
    transactions = filter_transactions(transactions, args.category, args.from_date, args.to_date)

    if not transactions:
        print("No transactions found.")
        return

    for transaction in transactions:
        print(
            f"{transaction.date} || "
            f"{transaction.category} || "
            f"{transaction.amount:_} ||".replace("_", " ") +
            f"{transaction.note if transaction.note else ""}"
        )


def handle_summary(args):
    transactions = load_transactions()
    for category, total in summarize_by_category(transactions).items():
        print(f"{category}: {total:_} ₸".replace("_", " "))
    print("--------------------")
    print(f"Total: {calculate_total(transactions):_} ₸.".replace("_", " "))


def _pick_transaction(transactions, category):
    matches = find_transactions(transactions, category)
    picked_transaction = questionary.select(
        "Select a transaction",
        choices=[
            Choice(
                title=(
                    f"{match.date} | "
                    f"{match.category} | "
                    f"{match.amount:_} ₸ | "
                    f"{match.note or ''}"
                ).replace("_", " "),
                value=match,
            )
            for match in matches
        ]
    ).ask()

    return picked_transaction


def handle_delete(args):
    picked_transaction = _pick_transaction(load_transactions(), args.category)
    delete_transaction_db(picked_transaction.id)
    print(f"Deleted transaction {picked_transaction.id}")


def handle_replace(args):
    picked_transaction = _pick_transaction(load_transactions(), args.category)
    new_transaction = create_transaction(
        amount=int(input("New amount: ") or picked_transaction.amount),
        category=input("New category: ") or picked_transaction.category,
        note=input("New note: ") or picked_transaction.note
    )

    replace_transaction(picked_transaction.id, new_transaction)
    print(f"Replace completed. New transaction: {new_transaction.id}")
