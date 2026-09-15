import argparse
from datetime import datetime

import questionary

from questionary import Choice

from tracker import (
    add_transaction,
    find_transactions,
    delete_transaction,
    calculate_total,
    load_transactions,
    save_transactions,
    summarize_by_category,
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
        args = parser.parse_args()

        transactions = load_transactions()

        if args.command == "add":
            transaction = add_transaction(transactions, args.amount, args.category, args.note)
            save_transactions(transactions)
            print(
                "Transaction added: "
                f"{transaction['category']} — {transaction['amount']:_} ₸"
                .replace("_", " ")
            )

        elif args.command == "delete":

            matches = find_transactions(transactions, args.category)
            removed_trans_id = questionary.select(
                "Select a transaction to remove",
                choices=[
                    Choice(
                        title=(
                            f"{match['date']} | "
                            f"{match['category']} | "
                            f"{match['amount']:_} ₸ | "
                            f"{match['note'] or ''}"
                        ).replace("_", " "),
                        value=match["id"],
                    )
                    for match in matches
                ]
            ).ask()

            removed_transaction = delete_transaction(transactions, removed_trans_id)
            save_transactions(transactions)

            print(f"Removed {removed_transaction['id']} "
                  f"|| {removed_transaction['date']} "
                  f"|| {removed_transaction['category']} "
                  f"|| {removed_transaction['amount']}"
                  )

        elif args.command == "list":
            display = []
            if args.category:
                transactions = [transaction for transaction in transactions if transaction["category"] == args.category]
            if args.to_date:
                transactions = [transaction for transaction in transactions if datetime.strptime(transaction["date"].split(" ")[0], "%Y-%m-%d") <= datetime.strptime(args.to_date, "%Y-%m-%d")]
            if args.from_date:
                transactions = [transaction for transaction in transactions if datetime.strptime(transaction["date"].split(" ")[0], "%Y-%m-%d") >= datetime.strptime(args.from_date, "%Y-%m-%d")]
            if not transactions:
                print("No transactions found.")

            else:
                for elem in transactions:
                    display.append(
                        f"{elem["date"]} || "
                        f"{elem["category"]} || "
                        f"{elem["amount"]:_} ||".replace("_", " ") +
                        f"{elem["note"] if elem["note"] else ""}"
                    )

            for x in display:
                print(x)

        elif args.command == "summary":
            for category, total in summarize_by_category(transactions).items():
                print(f"{category}: {total:_} ₸".replace("_", " "))
            print("--------------------")
            print(f"Total: {calculate_total(transactions):_} ₸.".replace("_", " "))
    except (ValueError, OSError) as error:
        print(f"Error: {error}")
        raise SystemExit(1)