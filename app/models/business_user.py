from app.models.base_model import BaseModel
from sqlalchemy import Column, String,Integer,Enum,Date
from app.helpers.enums import BusinessType,BusinessIndustry
from sqlalchemy.orm import relationship
from app.models.transactions import Transactions



class BusinessUser(BaseModel):
    __tablename__ = "business_users"
    business_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    business_type = Column(Enum(BusinessType), nullable=True)
    industry = Column(Enum(BusinessIndustry), nullable=True)
    registration_date = Column(Date, nullable=True)
    location = Column(String, nullable=True)
    no_of_employees = Column(Integer, nullable=True)

    transactions = relationship("Transactions", back_populates="business_user")

    







