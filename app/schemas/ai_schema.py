from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union, Literal
from datetime import datetime, date


class ExpenseData(BaseModel):
    category: str = Field(None, description="An expense category")
    amount: float = Field(..., description="Amount spent on the given category")

class Expense(BaseModel):
    utilities: float = Field(description="the amount spent on utilities")
    rent: float = Field(description="the amount spent on rent")
    payroll: float = Field(description="the amount spent on payroll")
    equipment: float = Field(description="the amount spent on equipment")

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
    liquidity_management: str = Field(description="Improve cash flow and ensure you have enough money to cover short-term expenses.")
    capital_structure_optimization: str = Field(description="Balance debt and equity to keep your business financially stable.")
    profitability_enhancements: str = Field(description="Increase profits by boosting revenue and cutting unnecessary costs.")
    operational_efficiency: str = Field(description="Streamline operations to reduce waste and improve productivity.")
    debt_management_risk_control: str = Field(description="Manage debt wisely to avoid financial stress and ensure stability.")


# 1. Profit and Loss Statement Schema
class OperatingExpenses(BaseModel):
    salaries: float = Field(..., description="Total employee salary and wage expenses")
    marketing: float = Field(..., description="Advertising and promotional campaign costs")
    rent_utilities: float = Field(..., description="Facility costs including electricity, water, and internet")
    depreciation: float = Field(..., description="Asset value reduction over time")
    insurance: float = Field(..., description="Business insurance premiums paid")
    professional_fees: float = Field(..., description="Legal, accounting, and consulting services costs")

class ProfitLossStatement(BaseModel):
    period_start: date = Field(..., description="Start date of reporting period (YYYY-MM-DD)")
    period_end: date = Field(..., description="End date of reporting period (YYYY-MM-DD)")
    total_revenue: float = Field(..., description="Gross sales before any deductions")
    cogs: float = Field(..., description="Direct costs of producing sold goods/services")
    gross_profit: float = Field(..., description="Revenue minus COGS (Total Revenue - COGS)")
    operating_expenses: OperatingExpenses = Field(..., description="Detailed breakdown of daily business costs")
    operating_income: float = Field(..., description="Profit before interest/taxes (Gross Profit - Operating Expenses)")
    interest_expense: Optional[float] = Field(0.0, description="Loan interest payments")
    tax_expense: float = Field(..., description="Income taxes paid to government")
    net_income: float = Field(..., description="Final profit/loss after all expenses")

# 2. Cash Flow Statement Schema  
class TransactionItem(BaseModel):
    description: str = Field(..., description="Transaction purpose/description (e.g., 'Office Equipment Purchase')")
    amount: float = Field(..., description="Transaction value in base currency")

class CashFlowStatement(BaseModel):
    reporting_period: str = Field(..., description="Fiscal period identifier (e.g., 'Q3 2024')")
    operating_activities: List[TransactionItem] = Field(..., description="Core business cash movements")
    investing_activities: List[TransactionItem] = Field(..., description="Asset-related transactions")
    financing_activities: List[TransactionItem] = Field(..., description="Funding/debt activities")
    net_cash_flow: float = Field(..., description="Sum of all cash movements (Operating + Investing + Financing)")
    beginning_cash: float = Field(..., description="Opening cash balance")
    ending_cash: float = Field(..., description="Closing cash balance (Beginning Cash + Net Cash Flow)")
    reconciliation_net_income: float = Field(..., description="Net income from P&L statement for verification")

# 3. Expense Report Schema
class ExpenseEntry(BaseModel):
    expense_date: date = Field(..., description="Date expense was incurred")
    category: str = Field(..., description="Expense type (e.g., Travel, Office Supplies)")
    description: str = Field(..., description="Detailed expense purpose")
    amount: float = Field(..., description="Expense value in base currency")
    vendor: str = Field(..., description="Merchant/supplier name")
    payment_method: str = Field(..., description="Payment type (Credit Card, Cash, etc.)")
    approved: bool = Field(..., description="Manager approval status")

class ExpenseReport(BaseModel):
    employee_name: str = Field(..., description="Claimant's full name")
    department: str = Field(..., description="Business unit/department")
    report_period: str = Field(..., description="Covered time period (e.g., 'March 2024')")
    expenses: List[ExpenseEntry] = Field(..., description="Individual expense items")
    total_amount: float = Field(..., description="Sum of all expenses")
    tax_deductible_total: float = Field(..., description="Eligible tax-deductible amount")
    reimbursement_requested: bool = Field(..., description="Employee repayment request status")

# 4. Income Report Schema
class RevenueStream(BaseModel):
    source: str = Field(..., description="Income origin (e.g., Product Sales, Services)")
    amount: float = Field(..., description="Revenue value in base currency")
    growth_rate: Optional[float] = Field(None, description="YOY percentage change")

class IncomeReport(BaseModel):
    fiscal_year: int = Field(..., description="Reporting fiscal year")
    revenue_streams: List[RevenueStream] = Field(..., description="Breakdown of income sources")
    cost_of_revenue: float = Field(..., description="Direct costs to generate revenue")
    gross_profit: float = Field(..., description="Revenue minus direct costs")
    operating_expenses: float = Field(..., description="Indirect business costs")
    ebitda: float = Field(..., description="Earnings Before Interest, Taxes, Depreciation & Amortization")
    net_profit: float = Field(..., description="Final profit after all deductions")
    yoy_growth: float = Field(..., description="Year-over-year total revenue change percentage")
    industry_benchmark: Optional[float] = Field(None, description="Sector average for comparison")