import sqlite3

import pytest
from _pytest import monkeypatch

import tracker
import database
from models import Transaction, ExpenseTracker
from exceptions import (
    TransactionNotFoundError,
    InvalidCategoryError,
    InvalidAmountError
)

from tracker import (
    create_transaction,
    filter_transactions,
    calculate_total
)

from database import (
    init_db,
    insert_transaction,
    insert_transactions_batch,
    delete_transaction,
    update_transaction,
    clear_transactions,
    replace_transaction
)
from unittest.mock import patch


# =====================================================FIXTURES=====================================================

@pytest.fixture
def transactions():
    return [
        Transaction(
            id="1",
            date="2026-09-10T12:00:00",
            amount=5000,
            category="food",
            note="Lunch"
        ),
        Transaction(
            id="2",
            date="2026-09-11T12:00:00",
            amount=3000,
            category="taxi",
        ),
        Transaction(
            id="3",
            date="2026-09-12T12:00:00",
            amount=4000,
            category="food",
        ),
    ]


@pytest.fixture
def example_tracker(transactions):
    fixture_tracker = ExpenseTracker()
    for transaction in transactions:
        fixture_tracker.add(transaction)
    return fixture_tracker


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"

    monkeypatch.setattr(
        database,
        "DB_FILE",
        test_db
    )

    init_db()

    return test_db


# =====================================================TESTS===========================================================

def test_calculate_total(transactions):
    result = calculate_total(transactions)
    assert result == 12000


def test_collection_calc_total_method(example_tracker):
    result = example_tracker.calc_total()
    assert result == 12000


def test_create_transaction():
    transaction = create_transaction(5000, "food", "Lunch")

    assert transaction.amount == 5000
    assert transaction.category == "food"
    assert transaction.note == "Lunch"


def test_insert_transaction(test_db, transactions):
    transaction = transactions[0]

    insert_transaction(transaction)
    loaded = database.load_transactions()

    assert loaded == [transaction]


def test_insert_transactions_batch(test_db, transactions):
    insert_transactions_batch(transactions)

    assert database.load_transactions() == transactions


def test_insert_batch_raises_integrity_error(test_db, transactions):
    transactions[2].id = "1"

    with pytest.raises(sqlite3.IntegrityError):
        insert_transactions_batch(transactions)

    assert database.load_transactions() == []


def test_formatted_amount(transactions):
    result = transactions[0].formatted_amount

    assert result == '5 000 ₸'


def test_create_transaction_calls_uuid_and_is_called_once():
    with patch("tracker.uuid.uuid4", return_value="fixed_id") as mock_uuid:
        transaction = tracker.create_transaction(
            5000,
            "food"
        )
    assert transaction.id == "fixed_id"
    mock_uuid.assert_called_once()


def test_load_transactions(test_db, transactions):
    for transaction in transactions:
        insert_transaction(transaction)
    loaded = database.load_transactions()

    assert test_db.exists()
    assert loaded == transactions


def test_load_empty_transactions(test_db):
    loaded = database.load_transactions()
    assert loaded == []


def test_update_transaction(test_db, transactions):
    transaction = transactions[0]
    insert_transaction(transaction)

    updated = update_transaction(
        transaction_id="1",
        amount=7777,
        category="books",
    )

    stored = database.load_transactions()[0]

    assert updated.amount == 7777
    assert updated.category == "books"

    assert updated.id == transaction.id
    assert updated.date == transaction.date
    assert updated.note == transaction.note

    assert stored == updated


def test_update_transaction_raises_nonexist_err(test_db):
    with pytest.raises(TransactionNotFoundError):
        update_transaction("5555")


def test_delete_transaction(test_db, transactions):
    transaction = transactions[0]
    insert_transaction(transaction)

    loaded = database.load_transactions()
    deleted = delete_transaction(transaction.id)

    assert loaded[0] == deleted


def test_delete_transaction_rejects_unknown_trans_id(test_db):
    trans_id = "unknown"

    with pytest.raises(TransactionNotFoundError):
        database.delete_transaction(trans_id)


def test_clear_transactions(test_db, transactions):
    for transaction in transactions:
        insert_transaction(transaction)

    assert len(database.load_transactions()) == 3

    clear_transactions()

    assert database.load_transactions() == []


@pytest.mark.parametrize("amount", [-5000, 0])
def test_create_transaction_rejects_invalid_amount(amount):
    with pytest.raises(InvalidAmountError):
        tracker.create_transaction(
            amount,
            "food"
        )


def test_transaction_instantiation_rejects_invalid_amount():
    with pytest.raises(InvalidAmountError):
        Transaction(
            id="1",
            date="2026-09-21",
            amount=-5000,
            category="food",
        )


@pytest.mark.parametrize("category", ["   ", ""])
def test_create_transaction_rejects_invalid_category(category):
    with pytest.raises(InvalidCategoryError):
        tracker.create_transaction(
            5000,
            category
        )


def test_filter_transactions_by_category(transactions):
    result = filter_transactions(
        transactions,
        category="  FOOD  "
    )

    assert len(result) == 2
    assert all(transaction.category == "food" for transaction in result)


def test_filter_transactions_from_date(transactions):
    result = filter_transactions(
        transactions,
        from_date="2026-09-11"
    )

    assert len(result) == 2
    assert result[0].date == "2026-09-11T12:00:00"
    assert result[1].date == "2026-09-12T12:00:00"


def test_replace_transaction(test_db, transactions):
    old_trans_id = transactions[0].id
    new_trans = create_transaction(5000, 'food')

    insert_transactions_batch(transactions)
    replace_transaction(old_trans_id, new_trans)

    loaded_ids = {trans.id for trans in database.load_transactions()}

    assert loaded_ids == {
        new_trans.id,
        transactions[1].id,
        transactions[2].id,
    }


def test_replace_transaction_rollback(test_db, transactions):
    pass