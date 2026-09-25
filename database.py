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
        rows = connection.execute(
            """
            SELECT *
            FROM transactions
            WHERE id = ?
            """,
            (transaction_id,),
        ).fetchall()

        if not rows:
            raise TransactionNotFoundError(f"Transaction with id {transaction_id} does not exist")

        connection.execute(
            """
            DELETE
            FROM transactions
            WHERE id = ?
            """,
            (transaction_id,)
        )

        return [Transaction(*row) for row in rows]