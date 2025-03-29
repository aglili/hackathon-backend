from app.models.transactions import Transactions


def transform_transaction_to_dict(transaction: Transactions) -> dict:
    """
    Transforms a Transactions object into a dictionary format.

    Args:
        transaction (Transactions): The Transactions object to transform.

    Returns:
        dict: A dictionary representation of the Transactions object.
    """
    return {
        "id": str(transaction.id),
        "user_id": str(transaction.user_id),
        "amount": transaction.amount,
        "transaction_type": transaction.transaction_type.value,
        "transaction_category": transaction.transaction_category.value,
        "description": transaction.description,
        "date": transaction.date.isoformat() if transaction.date else None,
    }