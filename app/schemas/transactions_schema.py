from pydantic import BaseModel
from datetime import date
from app.helpers.enums import TransactionType, TransactionCategory



class CreateTransactionRequestPartial(BaseModel):
    amount: float
    transaction_type: TransactionType
    transaction_category: TransactionCategory
    description: str
    date: date



class CreateTransactionRequest(CreateTransactionRequestPartial):
    user_id: str


