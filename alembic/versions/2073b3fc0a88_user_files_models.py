"""user files models

Revision ID: 2073b3fc0a88
Revises: 8ef93636a6cf
Create Date: 2025-03-29 10:11:22.978788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic.
revision: str = '2073b3fc0a88'
down_revision: Union[str, None] = '8ef93636a6cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "user_files",
        sa.Column("file_name", sa.String(), nullable=False),
        sa.Column("file_url", sa.String(), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("business_users.id"), nullable=False),
        sa.Column('id', UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid.uuid4, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user_files")
