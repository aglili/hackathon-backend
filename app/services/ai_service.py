from app.services.base_service import BaseService
from groq import Groq 
import pandas as pd 
import instructor
from app.schemas.ai_schema import Expense, Ratios, SmartProfile, ScoreImprovementRecommendations
from sklearn.ensemble import IsolationForest
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from app.config.settings import settings

client = instructor.from_groq(Groq(api_key=settings.GROQ_API_KEY))


class AIService():
    def __init__(self):
        super().__init__()

    

    def generate_expense_data(self, data_str: str):
        try:
            data = pd.read_csv(data_str)
            # Prepare analysis prompt
            prompt = f"""
            Analyze this business financial data:
            {data}
            
            Categorize expenses and calculate totals for:
            - Weekly expenses (divide monthly figures by 4)
            - Monthly expenses (direct figures)
            - Quarterly expenses (multiply monthly by 3)
            
            Return ONLY the structured JSON format with numerical values (no calculations in fields).
            """

            # Get structured LLM analysis
            analysis = client.chat.completions.create(
                messages=[
                        {
                                "role": "system",
                                "content": "You're a senior analysed tasked with expense categorization and aggregation"
                        },{
                                "role": "user",
                                "content": prompt
                        }
                ],
                model='llama3-8b-8192',
                temperature=0.2,
                response_model=Expense
            )

            #print(f'analysis: {analysis}')

            return analysis.dict()
        

        except Exception as e:
            #return FinancialAnalysisResult(error=f"Expense analysis failed: {str(e)}")
            print('error: ', e)



    def forecast_revenue(self, data_str: str, periods=6):
        """
        Forecast future revenue using ARIMA time series model.

        Parameters:
        - data (pd.DataFrame): Historical financial data containing 'Date' and 'Revenue'.
        - periods (int): Number of months to forecast.

        Returns:
        - forecast_df (pd.DataFrame): DataFrame containing predicted revenues.
        - model_fit: The trained ARIMA model.
        """
        data = pd.read_csv(data_str)
        # Convert Date column to datetime and set as index
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)

        # Ensure Revenue column is numeric
        data['Revenue'] = pd.to_numeric(data['Revenue'], errors='coerce')

        # Fit ARIMA Model (AutoRegressive Integrated Moving Average)
        model = ARIMA(data['Revenue'], order=(2,1,2))  # (p,d,q) values chosen based on assumption
        model_fit = model.fit()

        # Forecast future revenue
        forecast = model_fit.forecast(steps=periods)
        
        # Create DataFrame for predictions
        forecast_dates = pd.date_range(start=data.index[-1], periods=periods+1, freq='M')[1:]
        forecast_df = pd.DataFrame({'Date': forecast_dates, 'Predicted_Revenue': forecast.values})
    


        return {
            "date": forecast_dates,
            "predicted_revenue": forecast,
            "actual_revenue": data['Revenue']
        }

    def generate_financial_ratios(self, data_str: str):
        try:
            data = pd.read_csv(data_str)
            prompt = f"""
            Given the financial data of the company {data}. Your task is to generate as many financial ratios the provided data allows you to.
            - Liqudity ratios 
            - Leverage ratios
            - Solvency ratios 
            - Profitability and cash flow ratios 
            - credit and payment ratios

            Return ONLY the structured JSON format with numerical values (no calculations in fields).
            """
            analysis = client.chat.completions.create(
                messages=[
                        {
                                "role": "system",
                                "content": "You're a senior analysed tasked with generating financial ratios"
                        },{
                                "role": "user",
                                "content": prompt
                        }
                ],
                model='llama3-8b-8192',
                temperature=0.2,
                response_model=Ratios
            )
            return analysis.dict()
        except Exception as e:
            print('error: ', e)

    def generate_smart_profile(self, data_str: str):
        data = pd.read_csv(data_str)
        ratios = self.generate_financial_ratios(data)
        try:
            prompt = f"""
            Based on the financial ratios of the company {ratios}, consolidate the ratios and generate a score between 1 and 10 to represent.
            1. The business payment history: between 0 and 10
            2. revenue stability: betweeen 0 and 10
            3. debt to income ratio: betweeen 0 and 10
            4. business longetivity: betweeen 0 and 10
            5. smart_save_index: between 0 and 850

            then consolidate all the ratios into a risk assessment score that shows lenders how safe it is to offer the business a loan. 
            the risk assessment score should be between 0 and 850

            Return ONLY the structured JSON format with numerical values (no calculations in fields).
            """
            analysis = client.chat.completions.create(
                messages=[
                        {
                                "role": "system",
                                "content": "You're a senior analysed tasked with generating a comprehensive smart profile"
                        },{
                                "role": "user",
                                "content": prompt
                        }
                ],
                model='llama3-8b-8192',
                temperature=0.7,
                response_model=SmartProfile
            )
            return analysis
        except Exception as e:
            print('error: ', e)

    def generate_score_improvement_recommendations(self, data_str: str):
        data = pd.read_csv(data_str)
        risk_data = self.generate_financial_ratios(data)
        prompt = f"""
        Given the following financial ratios indicating the financial health of the business
        {risk_data}, create a recommendation on how to improve the business's financial ratios and overall risk assessment score.
        The recommendations should cover the following areas 
        - Liquidity Management 
        - Capital Structure Optimization
        - Profitability Enhancement
        - Operational Efficiency
        - Debt Management & Risk Control
        avoid using jargon and write out your recommendations for each section in a way a normal business owner would understand. make it very detailed but also simple

        Return ONLY the structured JSON format with numerical values (no calculations in fields).
        """
        response = client.chat.completions.create(
            messages=[
                        {
                                "role": "system",
                                "content": "You're a senior analysed tasked with creating score improvement recommendations"
                        },{
                                "role": "user",
                                "content": prompt
                        }
                ],
                model='llama3-8b-8192',
                temperature=0.7,
                response_model=ScoreImprovementRecommendations
        )
        return response