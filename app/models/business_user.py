from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, Enum, Date, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.helpers.enums import BusinessType, BusinessIndustry, RevenueRange
from sqlalchemy.orm import relationship
from app.models.transactions import Transactions
from app.models.reports import Businessreports

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
    revenue_range = Column(Enum(RevenueRange), nullable=False)
    in_debt = Column(Boolean, default=False)
    debt_range = Column(Enum(RevenueRange), nullable=True)

    transactions = relationship("Transactions", back_populates="business_user")
    user_files = relationship("UserFiles", back_populates="business_user")  # Fixed missing relationship
    reports = relationship("Businessreports", back_populates="business_user")

class UserFiles(BaseModel):
    __tablename__ = "user_files"

    file_name = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("business_users.id", ondelete="CASCADE"), nullable=False)

    business_user = relationship("BusinessUser", back_populates="user_files")
