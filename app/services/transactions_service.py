from fastapi import Depends
from app.repository.transactions_repository import TransactionsRepository
from app.services.base_service import BaseService
from app.models.business_user import BusinessUser
from app.schemas.transactions_schema import CreateTransactionRequestPartial,CreateTransactionRequest
from app.helpers.transformers.transactions_transformers import transform_transaction_to_dict
from app.helpers.enums import TransactionCategory,TransactionType
from app.helpers.utils import generate_pagination_metadata
from datetime import date




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


    async def get_transactions(self, user: BusinessUser,page: int = 1,limit: int =10,category: TransactionCategory = None,type: TransactionType = None,search_string : str = None,start_date: date =None,end_date: date = None) -> list:
        try:
            transactions = await self.repository.get_transactions(
                user_id=user.id,
                page=page,
                limit=limit,
                category=category,
                type=type,
                search_string=search_string,
                start_date=start_date,
                end_date=end_date
            )
            return {
                "transactions": [transform_transaction_to_dict(transaction=transaction) for transaction in transactions],
                "pagination": generate_pagination_metadata(
                    total_records=await self.repository.get_transactions_count(
                        user_id=user.id,
                        category=category,
                        type=type,
                        search_string=search_string,
                        start_date=start_date,
                        end_date=end_date
                    ),
                    page=page,
                    limit=limit
                )
            }
        except Exception as e:
            raise e
        


    async def get_overview(self, user: BusinessUser,start_date: date = None,end_date: date = None) -> dict:
        try:
            income,expenses,income_change,expenses_change = await self.repository.get_income_and_expense_totals(user_id=str(user.id),start_date=start_date,end_date=end_date)

            return {
                "income": income,
                "expenses": expenses,
                "income_change": income_change,
                "expenses_change": expenses_change
            }
            
        except Exception as e:
            raise e
        

    async def get_monthly_income_and_expenses(self,user:BusinessUser) -> dict:
        try:
            result = await self.repository.get_monthly_income_and_expenses(user_id=str(user.id))
            return result
        
        except Exception as e:
            raise e
        
        