import sqlite3
import logging

from pathlib import Path
from models import Transaction
from exceptions import TransactionNotFoundError

DB_FILE = Path(__file__).resolve().parent / "expenses.db"
logger = logging.getLogger(__name__)

UNSET = object()


def _insert_transaction(
        connection: sqlite3.Connection,
        transaction: Transaction
) -> None:
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


def _delete_transaction(
        connection: sqlite3.Connection,
        transaction_id: str
) -> Transaction:
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

    return Transaction(*row)


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
        _insert_transaction(connection, transaction)
    logger.info(
        "Transaction inserted: id=%s",
        transaction.id
    )


def insert_transactions_batch(transactions: list[Transaction]) -> None:
    with sqlite3.connect(DB_FILE) as connection:
        for transaction in transactions:
            _insert_transaction(connection, transaction)


def replace_transaction(
        old_transaction_id: str,
        new_transaction: Transaction
) -> Transaction:
    with sqlite3.connect(DB_FILE) as connection:
        _delete_transaction(connection, old_transaction_id)
        _insert_transaction(connection, new_transaction)
    logger.info(
        "Transaction id=%s replaced. New transaction id=%s",
        old_transaction_id, new_transaction.id
    )
    return new_transaction


def update_transaction(
        transaction_id: str,
        amount: int | None = UNSET,
        category: str | None = UNSET,
        note: str | None = UNSET
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

        def converter(new_value, old_value):
            if new_value is UNSET:
                return old_value
            return new_value

        new_amount, new_category, new_note = map(
            converter,
            [amount, category, note],
            [
                old_transaction.amount,
                old_transaction.category,
                old_transaction.note,
            ],
        )

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


def delete_transaction(transaction_id: str) -> Transaction:
    with sqlite3.connect(DB_FILE) as connection:
        deleted_transaction = _delete_transaction(connection, transaction_id)
    logger.info(
        "Transaction deleted: id=%s",
        deleted_transaction.id
    )
    return deleted_transaction


def clear_transactions() -> None:
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute(
            """
            DELETE
            FROM transactions
            """
        )
    logger.info("ALL transactions are deleted")
