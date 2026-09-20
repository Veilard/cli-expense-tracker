import pytest
import tracker
from models import Transaction

from tracker import (
    add_transaction,
    delete_transaction,
    filter_transactions,
    calculate_total
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
# =====================================================TESTS===========================================================

def test_calculate_total(transactions):
    result = calculate_total(transactions)

    assert result == 12000


def test_add_transaction():
    transactions = []

    transaction = add_transaction(
        transactions,
        5000,
        "Food",
        "Lunch"
    )

    assert transaction.amount == 5000
    assert transaction.category == "food"
    assert transaction.note == "Lunch"
    assert len(transactions) == 1


def test_add_transaction_calls_uuid_and_is_called_once():
    transactions = []

    with patch("tracker.uuid.uuid4", return_value="fixed_id") as mock_uuid:
        transaction = tracker.add_transaction(
            transactions,
            5000,
            "food"
        )
    assert transaction.id == "fixed_id"
    mock_uuid.assert_called_once()


def test_delete_transaction(transactions):
    removed_transaction = delete_transaction(transactions, "1")

    assert removed_transaction.id == "1"
    assert transactions[0].id == "2"
    assert len(transactions) == 2


def test_save_transactions(tmp_path, monkeypatch, transactions):
    test_file = tmp_path / "transactions.json"

    monkeypatch.setattr(
        tracker,
        "DATA_FILE",
        test_file
    )
    tracker.save_transactions(transactions)

    loaded = tracker.load_transactions()

    assert test_file.exists()
    assert loaded == transactions

def test_load_empty_transactions(tmp_path, monkeypatch):
    test_file = tmp_path / "transactions.json"

    monkeypatch.setattr(
        tracker,
        "DATA_FILE",
        test_file
    )

    loaded = tracker.load_transactions()
    assert loaded == []


def test_delete_transaction_rejects_unknown_trans_id(transactions):
    trans_id = "unknown"

    with pytest.raises(ValueError, match=f"Transaction with id {trans_id} does not exist"):
        tracker.delete_transaction(transactions, trans_id)


@pytest.mark.parametrize("amount", [-5000, 0])
def test_add_transaction_rejects_invalid_amount(amount):
    transactions = []

    with pytest.raises(ValueError, match="Invalid amount"):
        tracker.add_transaction(
            transactions,
            amount,
            "food"
        )


@pytest.mark.parametrize("category", ["   ", ""])
def test_add_transaction_rejects_invalid_category(category):
    transactions = []

    with pytest.raises(ValueError, match="Invalid category"):
        add_transaction(
            transactions,
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