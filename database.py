import sqlite3
from pathlib import Path
from models import Transaction
from exceptions import TransactionNotFoundError
from tracker import log_call

DB_FILE = Path(__file__).resolve().parent / "expenses.db"

def init_db() -> None:
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id TEXT PRIMARY KEY,
                date TEXT NOT NULL,
                amount INTEGER NOT NULL,
                category TEXT NOT NULL,
                note TEXT
            )
            """
        )


def insert_transaction(transaction: Transaction) -> None:
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute(
            """
            INSERT INTO transactions (
                id,
                date,
                amount,
                category,
                note
            )
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
def delete_transaction(transaction_id) -> None:
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.execute(
            """
            DELETE FROM transactions
            WHERE id = ?
            """,
            (transaction_id,)
        )

        if cursor.rowcount == 0:
            raise TransactionNotFoundError(f"Transaction with id {transaction_id} does not exist")