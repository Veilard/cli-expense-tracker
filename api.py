from fastapi import FastAPI
from schemas import TransactionResponse

from database import load_transactions

app = FastAPI()


@app.get("/health")
def health():
    return load_transactions()


@app.get(
    "/transactions",
    response_model=list[TransactionResponse]
)
def get_transactions():
    return load_transactions()