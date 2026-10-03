from fastapi import FastAPI

from schemas import (
    TransactionResponse,
    TransactionCreate
)

from database import (
    load_transactions,
    insert_transaction
)

from tracker import create_transaction

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


@app.post(
    "/transactions",
    response_model=TransactionResponse
)
def create_transaction_endpoint(data: TransactionCreate):
    transaction = create_transaction(data.amount, data.category, data.note)
    insert_transaction(transaction)
    return transaction
