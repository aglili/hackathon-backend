from sqlalchemy import Column, String, Integer, Enum,Float,Date,ForeignKey
from app.models.base_model import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from app.helpers.enums import TransactionType,TransactionCategory
from sqlalchemy.orm import relationship




class Transactions(BaseModel):
    __tablename__ = "transactions"
    user_id = Column(UUID(as_uuid=True), ForeignKey('business_users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    transaction_category = Column(Enum(TransactionCategory), nullable=False)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False)


    business_user = relationship("BusinessUser", back_populates="transactions")

    



