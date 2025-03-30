from app.models.reports import Businessreports





def transform_report_to_dict(report: Businessreports) -> dict:
    """
    Transform a report object into a dictionary format.
    """
    return {
        "id": str(report.id),
        "report_type": report.report_type,
        "report_data": report.report_data,
        "report_title": report.report_title,
        "created_at": report.created_at.isoformat(),
        "updated_at": report.updated_at.isoformat(),
    }