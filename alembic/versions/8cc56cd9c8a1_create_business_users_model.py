"""create business users model

Revision ID: 8cc56cd9c8a1
Revises: 
Create Date: 2025-03-29 01:16:22.047631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.helpers.enums import BusinessType, BusinessIndustry


# revision identifiers, used by Alembic.
revision: str = '8cc56cd9c8a1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'business_users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('business_name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), unique=True, nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('business_type', sa.Enum(BusinessType), nullable=True),
        sa.Column('industry', sa.Enum(BusinessIndustry), nullable=True),
        sa.Column('registration_date', sa.Date(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('no_of_employees', sa.Integer(), nullable=True),
    )

def downgrade():
    op.drop_table('business_users')

    op.execute("DROP TYPE IF EXISTS business_type")

    op.execute("DROP TYPE IF EXISTS business_industry")

