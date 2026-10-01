import argparse
import logging

from database import (
    init_db
)

from handlers import (
    handle_add,
    handle_list,
    handle_clear,
    handle_delete,
    handle_replace,
    handle_summary
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
delete_parser.set_defaults(func=handle_delete)

list_parser = subparser.add_parser("list")
list_parser.add_argument("--category", type=str)
list_parser.add_argument("--from_date", type=str)
list_parser.add_argument("--to_date", type=str)
list_parser.set_defaults(func=handle_list)

summary_parser = subparser.add_parser("summary")
summary_parser.set_defaults(func=handle_summary)

clear_parser = subparser.add_parser("clear")
clear_parser.set_defaults(func=handle_clear)

replace_parser = subparser.add_parser("replace")
replace_parser.add_argument("category", type=str)
replace_parser.set_defaults(func=handle_replace)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(__name__)
    try:
        init_db()
        args = parser.parse_args()
        args.func(args)
    except (ValueError, OSError) as error:
        logger.exception("Command execution failed")
        print(f"Error: {error}")
        raise SystemExit(1)


if __name__ == '__main__':
    main()
