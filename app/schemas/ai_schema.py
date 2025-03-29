from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union, Literal
from datetime import datetime


class ExpenseData(BaseModel):
    category: str = Field(None, description="An expense category")
    amount: float = Field(..., description="Amount spent on the given category")

class Expense(BaseModel):
    weekly: List[ExpenseData] = Field(description="a list of categorical expenses and amount spent on each categoty weekly")
    monthly: List[ExpenseData] = Field(description="a list of categorical expenses and amount spent on each categoty monthly")
    quarterly: List[ExpenseData] = Field(description="a list of categorical expenses and amount spent on each categoty quarterly")

class CashFlow(BaseModel):
    date: datetime = Field(description="date of the cash flow")
    cash_inflows: List[float] = Field(description="cash inflows")
    cash_outflows: List[float] = Field(description='cash outflows')
    cash_netflows: List[float] = Field(description="net cash flow calculated by subtracting cash outflow from cash inflow")


class RatioSample(BaseModel):
    ratio_name: str = Field(..., description="name of the ratio")
    value: float = Field(..., description="value of the ratio")

class Ratios(BaseModel):
    ratio: List[RatioSample] = Field(..., description="a list of financial ratios")

class SmartProfile(BaseModel):
    payment_history: float = Field(description=" a score between 0 and 10 representing the stability of the business payment history")
    revenue_stability: float = Field(description=" a score between 0 and 10 representing the stability of the business revenue")
    debt_income_ratio: float = Field(description=" a score between 0 and 10 representing the debt to income ratio of the business")
    business_longevity: float = Field(description=" a score between 0 and 10 representing the potential business longevity")
    smart_save_index: float = Field(description=" a score between 0 and 850 representing the risk assessment score of the business")

class ScoreImprovementRecommendations(BaseModel):
    liquidity_management = Field(description="Improve cash flow and ensure you have enough money to cover short-term expenses.")
    capital_structure_optimization = Field(description="Balance debt and equity to keep your business financially stable.")
    profitability_enhancements = Field(description="Increase profits by boosting revenue and cutting unnecessary costs.")
    operational_efficiency = Field(description="Streamline operations to reduce waste and improve productivity.")
    debt_management_risk_control = Field(description="Manage debt wisely to avoid financial stress and ensure stability.")