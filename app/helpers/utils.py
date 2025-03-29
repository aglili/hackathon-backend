


def generate_pagination_metadata(
    page: int, limit: int, total_records: int
) -> dict:
    """
    Generate pagination metadata for paginated responses.

    Args:
        page (int): Current page number.
        limit (int): Number of records per page.
        total_records (int): Total number of records.

    Returns:
        dict: A dictionary containing pagination metadata.
    """
    total_pages = (total_records + limit - 1) // limit  # Calculate total pages

    return {
        "current_page": page,
        "limit": limit,
        "total_pages": total_pages,
        "total_records": total_records,
    }
