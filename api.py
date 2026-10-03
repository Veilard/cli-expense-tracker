from fastapi import (
    FastAPI,
    HTTPException
)

from schemas import (
    TransactionResponse,
    TransactionCreate
)

from database import (
    load_transactions,
    insert_transaction
)

from tracker import (
    create_transaction,
    filter_transactions
)

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get(
    "/transactions",
    response_model=list[TransactionResponse]
)
def get_transactions():
    return load_transactions()


from fastapi import HTTPException


@app.get(
    "/transactions/category/{category}",
    response_model=list[TransactionResponse]
)
def filter_transactions_endpoint(category: str):
    result = filter_transactions(
        load_transactions(),
        category=category
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"No transactions found for category '{category}'"
        )

    return result


@app.post(
    "/transactions",
    response_model=TransactionResponse
)
def create_transaction_endpoint(data: TransactionCreate):
    transaction = create_transaction(data.amount, data.category, data.note)
    insert_transaction(transaction)
    return transaction
