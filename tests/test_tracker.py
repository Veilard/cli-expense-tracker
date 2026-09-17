import pytest
import tracker

from tracker import (
    add_transaction,
    delete_transaction,
    filter_transactions,
    calculate_total
)
# ------------------------------------------------FIXTURES-------------------------------------------------------------

@pytest.fixture
def transactions():
    return [
        {"category": "food","date": "2026-09-10T12:00:00"},
        {"category": "taxi","date": "2026-09-11T12:00:00"},
        {"category": "food","date": "2026-09-12T12:00:00"}
    ]

@pytest.fixture
def transactions_with_ids():
    return [
        {
            "id": "abc",
            "category": "food",
            "amount": 5000,
        },
        {
            "id": "def",
            "category": "taxi",
            "amount": 3000,
        },
    ]

# ------------------------------------------------TESTS-------------------------------------------------------------

def test_calculate_total():
    transactions = [
        {"amount": 1000},
        {"amount": 2500},
        {"amount": 500},
    ]

    result = calculate_total(transactions)

    assert result == 4000


def test_add_transaction():
    transactions = []

    transaction = add_transaction(
        transactions,
        5000,
        "Food",
        "Lunch"
    )

    assert transaction["amount"] == 5000
    assert transaction["category"] == "food"
    assert transaction["note"] == "Lunch"
    assert len(transactions) == 1


def test_delete_transaction(transactions_with_ids):
    removed_transaction = delete_transaction(transactions_with_ids, "abc")

    assert removed_transaction["id"] == "abc"
    assert transactions_with_ids[0]["id"] == "def"
    assert len(transactions_with_ids) == 1


def test_save_transactions(tmp_path, monkeypatch):
    test_file = tmp_path / "transactions.json"

    monkeypatch.setattr(
        tracker,
        "DATA_FILE",
        test_file
    )

    transactions = [
        {
            "id": "abc",
            "date": "2026-09-17T12:00:00",
            "amount": 5000,
            "category": "food",
            "note": "lunch",
        }
    ]

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




def test_delete_transaction_rejects_unknown_trans_id(transactions_with_ids):
    trans_id = "unknown"

    with pytest.raises(ValueError, match=f"Transaction with id {trans_id} does not exist"):
        tracker.delete_transaction(transactions_with_ids, trans_id)


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
    assert all(transaction["category"] == "food" for transaction in result)


def test_filter_transactions_from_date(transactions):
    result = filter_transactions(
        transactions,
        from_date="2026-09-11"
    )

    assert len(result) == 2
    assert result[0]["date"] == "2026-09-11T12:00:00"
    assert result[1]["date"] == "2026-09-12T12:00:00"