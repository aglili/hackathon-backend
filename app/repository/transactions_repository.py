from app.repository.base_repository import BaseRepository
from app.models.transactions import Transactions
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.config.database_config import get_db
from typing import Optional
from sqlalchemy import select
from app.helpers.enums import TransactionType, TransactionCategory
from datetime import date,timedelta
from calendar import month_name


class TransactionsRepository(BaseRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        super().__init__(Transactions, db)


    async def get_transactions(self,user_id:str,page:int= 1,limit: int = 10,category: Optional[TransactionCategory] = None,type: Optional[TransactionType] = None,search_string: Optional[str] = None,start_date : date = None,end_date: date = None) -> list:
        """
        Get transactions for a user with optional filters.
        """
        stmt = select(self.model).where(self.model.user_id == user_id)
        
        if category:
            stmt = stmt.where(self.model.transaction_category == category)
        
        if type:
            stmt = stmt.where(self.model.transaction_type == type)
        
        if search_string:
            stmt = stmt.where(self.model.description.ilike(f"%{search_string}%"))


        if start_date and end_date:
            stmt = stmt.where(self.model.date.between(start_date, end_date))


        stmt = stmt.order_by(self.model.created_at.desc()) 
        
        result = await self.db.execute(stmt.limit(limit).offset((page - 1) * limit))
        return result.scalars().all()
    


    async def get_transactions_count(self, user_id: str, category: Optional[TransactionCategory] = None, type: Optional[TransactionType] = None, search_string: Optional[str] = None, start_date: date = None, end_date: date = None) -> int:
        """
        Get the count of transactions for a user with optional filters,  including date range.
        """
        stmt = select(self.model).where(self.model.user_id == user_id)
        
        if category:
            stmt = stmt.where(self.model.transaction_category == category)
        
        if type:
            stmt = stmt.where(self.model.transaction_type == type)
        
        if search_string:
            stmt = stmt.where(self.model.description.ilike(f"%{search_string}%"))

        if start_date and end_date:
            stmt = stmt.where(self.model.date.between(start_date, end_date))
        
        result = await self.db.execute(stmt)
        return len(result.scalars().all())
    


    async def get_income_and_expense_totals(self, user_id: str, start_date: date = None, end_date: date = None) -> tuple:
        """
        Calculates the total income and expenses for a given user, with optional date range,
        and calculates the percentage change compared to the previous period if start and end dates are provided.

        Args:
            user_id (str): The ID of the user.
            start_date (date, optional): The start date for the transaction period. Defaults to None.
            end_date (date, optional): The end date for the transaction period. Defaults to None.

        Returns:
            tuple: (income, expenses, income_change, expenses_change)
                   - income (float): Total income for the period.
                   - expenses (float): Total expenses for the period.
                   - income_change (float): Percentage change in income compared to the previous period (or None if no date range).
                   - expenses_change (float): Percentage change in expenses compared to the previous period (or None if no date range).
        """

        stmt = select(self.model.amount, self.model.transaction_type).where(self.model.user_id == user_id)

        if start_date and end_date:
            stmt = stmt.where(self.model.date.between(start_date, end_date))

        result = await self.db.execute(stmt)
        transactions = result.all()

        income = 0
        expenses = 0

        for amount, transaction_type in transactions:
            if transaction_type == TransactionType.INCOME:
                income += amount
            elif transaction_type == TransactionType.EXPENSE:
                expenses += amount

        income_change = None
        expenses_change = None

        if start_date and end_date:
            # Calculate the previous period
            time_delta = end_date - start_date
            prev_end_date = start_date - timedelta(days=1)
            prev_start_date = prev_end_date - time_delta

            # Recursive call to get totals for the previous period
            prev_income, prev_expenses, _, _ = await self.get_income_and_expense_totals(user_id, prev_start_date, prev_end_date) 

            if prev_income != 0:
                income_change = ((income - prev_income) / prev_income) * 100
            else:
                income_change = None  

            if prev_expenses != 0:
                expenses_change = ((expenses - prev_expenses) / prev_expenses) * 100
            else:
                 expenses_change = None 

        return income, expenses, income_change, expenses_change
    



    async def get_monthly_income_and_expenses(self, user_id: str) -> dict:
        """
        Calculates the total income and expenses for each month over the past year for a given user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            dict: A dictionary where keys are month names (e.g., "January") and values are dictionaries
                  containing the total income and expenses for that month.
                  Example:
                  {
                    "January": {"income": 1000.00, "expenses": 500.00},
                    "February": {"income": 1200.00, "expenses": 600.00},
                    ...
                  }
        """

        today = date.today()
        one_year_ago = today - timedelta(days=365)

        # Initialize the result dictionary
        monthly_data = {month: {"income": 0, "expenses": 0} for month in month_name[1:]}  # Exclude the empty string at month_name[0]

        stmt = select(self.model.amount, self.model.transaction_type, self.model.date).where(
            self.model.user_id == user_id,
            self.model.date >= one_year_ago,
            self.model.date <= today
        )
        result = await self.db.execute(stmt)
        transactions = result.all()

        for amount, transaction_type, transaction_date in transactions:
            month = month_name[transaction_date.month]  # Get the month name
            if transaction_type == TransactionType.INCOME:
                monthly_data[month]["income"] += amount
            elif transaction_type == TransactionType.EXPENSE:
                monthly_data[month]["expenses"] += amount

        return monthly_data

