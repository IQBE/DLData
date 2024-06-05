"""update todo table

Revision ID: 7b24ffab2cf1
Revises: 34f1c91db126
Create Date: 2024-05-30 14:17:05.741044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b24ffab2cf1'
down_revision: Union[str, None] = '34f1c91db126'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("todos", sa.Column("completed", sa.Boolean, server_default=sa.text("false")))


def downgrade() -> None:
    op.drop_column("todos", "completed")
