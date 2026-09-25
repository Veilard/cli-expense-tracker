import argparse
import questionary

from questionary import Choice
from tracker import (
    create_transaction,
    find_transactions,
    filter_transactions,
    calculate_total,
    summarize_by_category,
)
from database import (
    init_db,
    insert_transaction,
    load_transactions,
    delete_transaction as delete_transaction_db
)

parser = argparse.ArgumentParser(description="Track expense tracker")
subparser = parser.add_subparsers(dest="command", required=True)

add_parser = subparser.add_parser("add")
add_parser.add_argument("amount", type=int, )
add_parser.add_argument("category", type=str)
add_parser.add_argument("--note", type=str)

delete_parser = subparser.add_parser("delete")
delete_parser.add_argument("category", type=str)

list_parser = subparser.add_parser("list")
list_parser.add_argument("--category", type=str)
list_parser.add_argument("--from_date", type=str)
list_parser.add_argument("--to_date", type=str)

summary_parser = subparser.add_parser("summary")

if __name__ == '__main__':
    try:
        init_db()
        args = parser.parse_args()

        transactions = load_transactions()

        if args.command == "add":
            transaction = create_transaction(args.amount, args.category, args.note)
            insert_transaction(transaction)
            print(
                "Transaction added: "
                f"{transaction.category} — {transaction.amount:_} ₸"
                .replace("_", " ")
            )

        elif args.command == "delete":
            matches = find_transactions(transactions, args.category)
            removed_trans_id = questionary.select(
                "Select a transaction to remove",
                choices=[
                    Choice(
                        title=(
                            f"{match.date} | "
                            f"{match.category} | "
                            f"{match.amount:_} ₸ | "
                            f"{match.note or ''}"
                        ).replace("_", " "),
                        value=match.id,
                    )
                    for match in matches
                ]
            ).ask()

            delete_transaction_db(removed_trans_id)

        elif args.command == "list":
            transactions = filter_transactions(transactions, args.category, args.from_date, args.to_date)
            if not transactions:
                print("No transactions found.")
                
            for transaction in transactions:
                print(
                    f"{transaction.date} || "
                    f"{transaction.category} || "
                    f"{transaction.amount:_} ||".replace("_", " ") +
                    f"{transaction.note if transaction.note else ""}"
                )

        elif args.command == "summary":
            for category, total in summarize_by_category(transactions).items():
                print(f"{category}: {total:_} ₸".replace("_", " "))
            print("--------------------")
            print(f"Total: {calculate_total(transactions):_} ₸.".replace("_", " "))
    except (ValueError, OSError) as error:
        print(f"Error: {error}")
        raise SystemExit(1)