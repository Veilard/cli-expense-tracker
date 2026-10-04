from datetime import date

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
def filter_transactions_endpoint(
        category: str | None = None,
        from_date: date | None = None,
        to_date: date | None = None
):
    result = filter_transactions(
        load_transactions(),
        category,
        from_date,
        to_date
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No transactions found"
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
