import sqlite3
from pathlib import Path
from models import Transaction
from exceptions import TransactionNotFoundError
from decorators import log_call

DB_FILE = Path(__file__).resolve().parent / "expenses.db"


def init_db() -> None:
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions
            (
                id
                TEXT
                PRIMARY
                KEY,
                date
                TEXT
                NOT
                NULL,
                amount
                INTEGER
                NOT
                NULL,
                category
                TEXT
                NOT
                NULL,
                note
                TEXT
            )
            """
        )


def insert_transaction(transaction: Transaction) -> None:
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute(
            """
            INSERT INTO transactions (id,
                                      date,
                                      amount,
                                      category,
                                      note)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                transaction.id,
                transaction.date,
                transaction.amount,
                transaction.category,
                transaction.note
            )
        )


def update_transaction(
        transaction_id: str,
        amount: int | None = None,
        category: str | None = None,
        note: str | None = None
) -> Transaction:
    with sqlite3.connect(DB_FILE) as connection:
        row = connection.execute(
            """
            SELECT id, date, amount, category, note
            FROM transactions
            WHERE id = ?
            """,
            (transaction_id,)
        ).fetchone()

        if row is None:
            raise TransactionNotFoundError(f"Transaction with id {transaction_id} does not exist")

        old_transaction = Transaction(*row)

        new_amount = amount if amount is not None else old_transaction.amount
        new_category = category if category is not None else old_transaction.category
        new_note = note if note is not None else old_transaction.note

        updated_transaction = Transaction(
            old_transaction.id,
            old_transaction.date,
            new_amount,
            new_category,
            new_note
        )

        connection.execute(
            """
            UPDATE transactions
            SET amount   = ?,
                category = ?,
                note     = ?
            WHERE id = ?
            """,
            (
                updated_transaction.amount,
                updated_transaction.category,
                updated_transaction.note,
                transaction_id
            )
        )

        return updated_transaction


def load_transactions() -> list[Transaction]:
    with sqlite3.connect(DB_FILE) as connection:
        rows = connection.execute(
            """
            SELECT id, date, amount, category, note
            FROM transactions
            """
        ).fetchall()

        return [Transaction(*row) for row in rows]


@log_call
def delete_transaction(transaction_id: str) -> list[Transaction]:
    with sqlite3.connect(DB_FILE) as connection:
        row = connection.execute(
            """
            SELECT *
            FROM transactions
            WHERE id = ?
            """,
            (transaction_id,)
        ).fetchone()

        if not row:
            raise TransactionNotFoundError(f"Transaction with id {transaction_id} does not exist")

        connection.execute(
            """
            DELETE
            FROM transactions
            WHERE id = ?
            """,
            (transaction_id,)
        )

        return [Transaction(*row)]


def clear_transactions(user_answer: str) -> None:
    if user_answer == 'Yes':
        with sqlite3.connect(DB_FILE) as connection:
            connection.execute(
                """
                DELETE FROM transactions
                """
            )
        print("ALL transactions are deleted")