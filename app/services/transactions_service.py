from fastapi import Depends
from app.repository.transactions_repository import TransactionsRepository
from app.services.base_service import BaseService
from app.models.business_user import BusinessUser
from app.schemas.transactions_schema import CreateTransactionRequestPartial,CreateTransactionRequest
from app.helpers.transformers.transactions_transformers import transform_transaction_to_dict




class TransactionsService(BaseService):
    def __init__(self, repository: TransactionsRepository = Depends(TransactionsRepository)) -> None:
        self.repository = repository
        super().__init__(repository)




    async def create_transaction(self,user:BusinessUser, payload:CreateTransactionRequestPartial) -> dict:
        try:
            schema = CreateTransactionRequest(
                amount=payload.amount,
                transaction_type=payload.transaction_type,
                transaction_category=payload.transaction_category,
                date=payload.date,
                description=payload.description,
                user_id=str(user.id)
            )

            transaction = await self.repository.create(schema)
            return transform_transaction_to_dict(transaction=transaction)
        except Exception as e:
            raise e
