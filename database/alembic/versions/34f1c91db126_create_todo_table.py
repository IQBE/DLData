"""create todo table

Revision ID: 34f1c91db126
Revises:
Create Date: 2024-05-30 14:00:43.616834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34f1c91db126'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "todos",
        sa.Column("todo_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(50), nullable=False),
        sa.Column("description", sa.Unicode(255)),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime, server_default=sa.text("now()"), nullable=False)
    )


def downgrade() -> None:
    op.drop_table("todos")