"""align users table with model

Revision ID: 009414521c7d
Revises: a4510eefdf1a
Create Date: 2026-09-27 23:06:05.948372
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '009414521c7d'
down_revision: Union[str, None] = 'a4510eefdf1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users", "full_name", new_column_name="name")
    op.alter_column("users", "is_active", new_column_name="status")
    op.add_column("users", sa.Column("profile", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "profile")
    op.alter_column("users", "status", new_column_name="is_active")
    op.alter_column("users", "name", new_column_name="full_name")
