from app.models.business_user import BusinessUser

def transform_user_to_dict(user: BusinessUser) -> dict:
    """
    Convert a BusinessUser model instance into a dictionary.
    """
    return {
        "id": str(user.id),
        "email": user.email,
        "business_name": user.business_name or None,
        "business_type": user.business_type.value if user.business_type else None,
        "industry": user.industry.value if user.industry else None,
        "registration_date": user.registration_date.isoformat() if user.registration_date else None,
        "location": user.location or None,
        "no_of_employees": user.no_of_employees or None,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
        "has_been_fully_onboarded": all([
            user.business_name,
            user.business_type,
            user.industry,
            user.registration_date,
            user.location
        ])
    }
