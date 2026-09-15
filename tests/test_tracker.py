from tracker import (calculate_total, add_transaction)

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