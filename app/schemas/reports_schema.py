from pydantic import BaseModel
from app.helpers.enums import ReportType


class CreateReport(BaseModel):
    user_id: str
    report_type: ReportType
    report_data: dict