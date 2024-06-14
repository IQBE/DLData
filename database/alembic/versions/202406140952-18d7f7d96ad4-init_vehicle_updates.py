"""init vehicle updates

Revision ID: 18d7f7d96ad4
Revises: 
Create Date: 2024-06-14 09:52:26.712962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18d7f7d96ad4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('vehicle_updates',
                    sa.Column('trip_id', sa.String(), nullable=False),
                    sa.Column('departure_delay', sa.Integer(), nullable=True),
                    sa.Column('departure_stop_id', sa.String(), nullable=True),
                    sa.Column('vehicle', sa.String(), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('trip_id')
                    )


def downgrade() -> None:
    op.drop_table('vehicle_updates')
