from sqlalchemy import Column,Enum,ForeignKey,JSON
from app.models.base_model import BaseModel
from app.helpers.enums import ReportType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship




class Businessreports(BaseModel):
    __tablename__ = 'business_reports'
    report_type = Column(Enum(ReportType),nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('business_users.id'), nullable=False)
    report_data = Column(JSON, nullable=False)
    business_user = relationship("BusinessUser", back_populates="reports")
