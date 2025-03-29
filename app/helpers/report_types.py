from app.schemas.ai_schema import *
import json

def return_report(report, data):
    reports = {
        "profit_loss": {
            "system_prompt": "You are a certified public accountant specializing in GAAP-compliant Profit and Loss Statement preparation. Your analyses are precise, comprehensive, and adhere to the latest accounting standards. You meticulously categorize all income and expenses while maintaining audit-ready documentation. Return a JSON file only",
            "user_prompt": f"Using the following business financial data: {data}, generate a comprehensive Profit and Loss Statement with the schema {json.dumps(ProfitLossStatement.schema())}",
            "response_model": ProfitLossStatement 
        },
        "cash_flow": {
            "system_prompt": "You are a corporate financial analyst with 15 years of experience in cash flow management and liquidity analysis. Your expertise includes direct/indirect method conversions and working capital optimization strategies recognized by the CFA Institute. Return a JSON file only",
            "user_prompt": f"Analyze the provided business transaction records: {data} and generate a detailed Cash Flow Statement with the following schema: {json.dumps(CashFlowStatement.schema())}",
            "response_model": CashFlowStatement 
        },
        "expense": {
            "system_prompt": "You are an audit-grade expense reporting specialist with deep knowledge of IRS publication 463 and corporate travel policy compliance. Your reports maintain perfect audit trails while identifying potential policy violations. Return a JSON file only",
            "user_prompt": f"Process these raw expense records: {data} into a standardized Expense Report. use the schema: {json.dumps(ExpenseReport.schema())}.",
            "response_model": ExpenseReport
        },
        "income": {
            "system_prompt": "You are a Fortune 500 financial strategist specializing in income analysis and comparative benchmarking. Your reports combine SEC filing rigor with actionable business insights for executive decision-making. Return a JSON file only",
            "user_prompt": f"Transform the raw financial data: {data} into a professional Income Report. use the schema: {json.dumps(IncomeReport.schema())}",
            "response_model": IncomeReport 
        }
    }

    return reports[report]