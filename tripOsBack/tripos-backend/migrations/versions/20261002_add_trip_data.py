"""add JSON data to trips

Revision ID: 20261002_trip_data
Revises: 61eb90155a05
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20261002_trip_data"
down_revision: Union[str, None] = "61eb90155a05"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "trips",
        sa.Column("data", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
    )
    op.alter_column("trips", "data", server_default=None)


def downgrade() -> None:
    op.drop_column("trips", "data")
