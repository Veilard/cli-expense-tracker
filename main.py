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
    delete_transaction as delete_transaction_db,
    clear_transactions,
    replace_transaction
)

from handlers import (
    handle_add,
    handle_list,
    handle_clear
)

parser = argparse.ArgumentParser(description="Track expense tracker")
subparser = parser.add_subparsers(dest="command", required=True)

add_parser = subparser.add_parser("add")
add_parser.add_argument("amount", type=int, )
add_parser.add_argument("category", type=str)
add_parser.add_argument("--note", type=str)
add_parser.set_defaults(func=handle_add)

delete_parser = subparser.add_parser("delete")
delete_parser.add_argument("category", type=str)

list_parser = subparser.add_parser("list")
list_parser.add_argument("--category", type=str)
list_parser.add_argument("--from_date", type=str)
list_parser.add_argument("--to_date", type=str)
list_parser.set_defaults(func=handle_list)

summary_parser = subparser.add_parser("summary")

clear_parser = subparser.add_parser("clear")
clear_parser.set_defaults(func=handle_clear)

replace_parser = subparser.add_parser("replace")
replace_parser.add_argument("category", type=str)

if __name__ == '__main__':
    try:
        init_db()
        args = parser.parse_args()
        args.func(args)


        #
        # elif args.command in ["replace", "delete"]:
        #     matches = find_transactions(transactions, args.category)
        #     picked_transaction_id = questionary.select(
        #         "Select a transaction",
        #         choices=[
        #             Choice(
        #                 title=(
        #                     f"{match.date} | "
        #                     f"{match.category} | "
        #                     f"{match.amount:_} ₸ | "
        #                     f"{match.note or ''}"
        #                 ).replace("_", " "),
        #                 value=match.id,
        #             )
        #             for match in matches
        #         ]
        #     ).ask()
        #
            # if args.command == 'delete':
            #     delete_transaction_db(picked_transaction_id)
            #     print(f"Deleted transaction {picked_transaction_id}")
            # else:
            #     picked_transaction = [match for match in matches if match.id == picked_transaction_id][0]
            #     new_transaction = create_transaction(
            #         amount=int(input("New amount: ") or picked_transaction.amount),
            #         category=input("New category: ") or picked_transaction.category,
            #         note=input("New note: ") or picked_transaction.note
            #     )
            #
            #     replace_transaction(picked_transaction_id, new_transaction)
            #     print(f"Replace completed. New transaction: {new_transaction.id}")


        # elif args.command == "summary":
        #     for category, total in summarize_by_category(transactions).items():
        #         print(f"{category}: {total:_} ₸".replace("_", " "))
        #     print("--------------------")
        #     print(f"Total: {calculate_total(transactions):_} ₸.".replace("_", " "))
    except (ValueError, OSError) as error:
        print(f"Error: {error}")
        raise SystemExit(1)
