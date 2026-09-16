import pytest

from tracker import (
    calculate_total,
    add_transaction,
    filter_transactions
)

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

@pytest.mark.parametrize("amount", [-5000, 0])
def test_add_transaction_rejects_invalid_amount(amount):
    transactions = []

    with pytest.raises(ValueError, match="Invalid amount"):
        add_transaction(
            transactions,
            amount,
            "food"
        )

@pytest.mark.parametrize("cat", ["   ", "", 123])
def test_add_transaction_rejects_invalid_category():
    transactions = []

    with pytest.raises(ValueError, match="Invalid category"):
        add_transaction(
            transactions,
            5000,
            cat
        )

@pytest.fixture
def transactions():
    return [
        {"category": "food","date": "2026-09-10T12:00:00"},
        {"category": "taxi","date": "2026-09-11T12:00:00"},
        {"category": "food","date": "2026-09-12T12:00:00"}
    ]

def test_filter_transactions_by_category():

    result = filter_transactions(
        transactions,
        category="  FOOD  "
    )

    assert len(result) == 2
    assert all(transaction["category"] == "food" for transaction in result)


def test_filter_transactions_from_date():
    result = filter_transactions(
        transactions,
        from_date="2026-09-11"
    )

    assert len(result) == 2
    assert result[0]["date"] == "2026-09-11T12:00:00"
    assert result[1]["date"] == "2026-09-12T12:00:00"