"""add destination lifecycle and AI usage telemetry

Revision ID: 20261013_admin_ai_usage
Revises: 20261011_admin_reports_audit
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20261013_admin_ai_usage"
down_revision: Union[str, None] = "20261011_admin_reports_audit"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "destinations",
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="published",
        ),
    )

    op.create_table(
        "ai_usage_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("succeeded", sa.Boolean(), nullable=False),
        sa.Column("duration_ms", sa.Integer(), nullable=False),
        sa.Column("input_tokens", sa.Integer(), nullable=True),
        sa.Column("output_tokens", sa.Integer(), nullable=True),
        sa.Column("error_type", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_usage_events_id", "ai_usage_events", ["id"], unique=False)
    op.create_index(
        "ix_ai_usage_events_succeeded",
        "ai_usage_events",
        ["succeeded"],
        unique=False,
    )
    op.create_index(
        "ix_ai_usage_events_created_at",
        "ai_usage_events",
        ["created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_ai_usage_events_created_at", table_name="ai_usage_events")
    op.drop_index("ix_ai_usage_events_succeeded", table_name="ai_usage_events")
    op.drop_index("ix_ai_usage_events_id", table_name="ai_usage_events")
    op.drop_table("ai_usage_events")
    op.drop_column("destinations", "status")
