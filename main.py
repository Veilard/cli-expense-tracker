import argparse

from tracker import (
    add_transaction,
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
            removed_transaction = delete_transaction(transactions, args.category)
            save_transactions(transactions)
            print(
                "Transaction deleted: "
                f"{removed_transaction["id"]} — {removed_transaction['category']} — {removed_transaction['amount']:_} ₸"
                .replace("_", " ")
            )


        elif args.command == "list":
            if not transactions:
                print("No transactions found.")
            else:
                for elem in transactions:
                    print(
                        f"{elem["date"]} || "
                        f"{elem["category"]} || "
                        f"{elem["amount"]:_} ||".replace("_", " "),
                        f"{elem["note"] if elem["note"] else ""}"
                    )

        elif args.command == "summary":
            for category, total in summarize_by_category(transactions).items():
                print(f"{category}: {total:_} ₸".replace("_", " "))
            print("--------------------")
            print(f"Total: {calculate_total(transactions):_} ₸.".replace("_", " "))
    except (ValueError, OSError) as error:
        print(f"Error: {error}")
        raise SystemExit(1)