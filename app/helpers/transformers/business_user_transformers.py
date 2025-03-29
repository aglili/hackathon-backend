from app.models.business_user import BusinessUser



def transform_user_to_dict(user: BusinessUser) -> dict:
    """
    Transform a Business User model instance to a dictionary.
    """
    return {
        "id": str(user.id),
        "email": user.email,
        "business_name": user.business_name if user.business_name else None,
        "business_type": user.business_type.value if user.business_type else None,
        "industry": user.industry.value if user.industry else None,
        "registration_date": user.registration_date.isoformat() if user.registration_date else None,
        "location": user.location if user.location else None,
        "no_of_employees": user.no_of_employees if user.no_of_employees else None,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat()
    }