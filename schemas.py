from pydantic import BaseModel, ConfigDict

class TransactionResponse(BaseModel):
    id: str
    date: str
    amount: int
    category: str
    note: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TransactionCreate(BaseModel):
    amount: int
    category: str
    note: str | None = None
