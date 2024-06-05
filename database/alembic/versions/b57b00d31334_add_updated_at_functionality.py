"""Add updated_at functionality

Revision ID: b57b00d31334
Revises: 7b24ffab2cf1
Create Date: 2024-06-05 13:27:06.372383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b57b00d31334'
down_revision: Union[str, None] = '7b24ffab2cf1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("todos", "updated_at", onupdate=sa.text("now()"))


def downgrade() -> None:
    op.alter_column("todos", "updated_at", onupdate=None)
