from enum import Enum



class BusinessType(str, Enum):
    """
    Enum for business types.
    """
    SOLE_PROPRIETORSHIP = "Sole Proprietorship"
    PARTNERSHIP = "Partnership"
    CORPORATION = "Corporation"
    LIMITED_LIABILITY_COMPANY = "Limited Liability Company (LLC)"
    NON_PROFIT = "Non-Profit Organization"


class BusinessIndustry(str, Enum):
    """
    Enum for business industries.
    """
    TECHNOLOGY = "Technology"
    HEALTHCARE = "Healthcare"
    FINANCE = "Finance"
    RETAIL = "Retail"
    MANUFACTURING = "Manufacturing"
    EDUCATION = "Education"
    REAL_ESTATE = "Real Estate"
    ENTERTAINMENT = "Entertainment"
    FOOD_AND_BEVERAGE = "Food and Beverage"
    TRANSPORTATION = "Transportation"



class TransactionType(str, Enum):
    """
    Enum for transaction types.
    """
    INCOME = "income"
    EXPENSE = "expense"



class TransactionCategory(str, Enum):
    """
    Enum for transaction categories.
    """
    SALARY = "salary"
    INVESTMENT = "investment"
    SALES = "sales"
    RENT = "rent"
    UTILITIES = "utilities"
    SUPPLIES = "supplies"
    MARKETING = "marketing"
    TRAVEL = "travel"
    OTHER = "other"
