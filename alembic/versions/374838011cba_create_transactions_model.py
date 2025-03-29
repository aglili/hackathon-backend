"""create transactions  model

Revision ID: 374838011cba
Revises: 8cc56cd9c8a1
Create Date: 2025-03-29 03:23:18.320256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.helpers.enums import TransactionType, TransactionCategory


# revision identifiers, used by Alembic.
revision: str = '374838011cba'
down_revision: Union[str, None] = '8cc56cd9c8a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'transactions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('business_users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('transaction_type', sa.Enum(TransactionType), nullable=False),
        sa.Column('transaction_category', sa.Enum(TransactionCategory), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
    )


def downgrade() -> None:
    
    """Downgrade schema."""
    op.drop_table('transactions')

    op.execute("DROP TYPE IF EXISTS transaction_type")

    op.execute("DROP TYPE IF EXISTS transaction_category")
