"""alter business users model

Revision ID: 8ef93636a6cf
Revises: 374838011cba
Create Date: 2025-03-29 06:37:08.763171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.helpers.enums import RevenueRange


# revision identifiers, used by Alembic.
revision: str = '8ef93636a6cf'
down_revision: Union[str, None] = '374838011cba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'business_users',
        sa.Column('revenue_range', sa.Enum(RevenueRange), nullable=True),
    )
    op.add_column(
        'business_users',
        sa.Column('in_debt', sa.Boolean(), default=False),
    )
    op.add_column(
        'business_users',
        sa.Column('debt_range', sa.Enum(RevenueRange), nullable=True),
    )
    op.create_index('ix_business_users_revenue_range', 'business_users', ['revenue_range'])
    op.create_index('ix_business_users_in_debt', 'business_users', ['in_debt'])
    op.create_index('ix_business_users_debt_range', 'business_users', ['debt_range'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_business_users_revenue_range', 'business_users')
    op.drop_index('ix_business_users_in_debt', 'business_users')
    op.drop_index('ix_business_users_debt_range', 'business_users')
    op.drop_column('business_users', 'revenue_range')
    op.drop_column('business_users', 'in_debt')
    op.drop_column('business_users', 'debt_range')
    

