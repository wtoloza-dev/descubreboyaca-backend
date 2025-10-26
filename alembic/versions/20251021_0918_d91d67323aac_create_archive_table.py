"""Create archive table.

Revision ID: d91d67323aac
Revises:
Create Date: 2025-10-21 09:18:18.926692

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "d91d67323aac"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create archive table for soft-deleted records.

    This table stores deleted records from any entity table, preserving
    all data as JSON for audit and recovery purposes.
    """
    op.create_table(
        "archive",
        # Primary key (ULID)
        sa.Column("id", sa.String(length=26), nullable=False),
        # Original record metadata
        sa.Column("original_table", sa.String(length=255), nullable=False),
        sa.Column("original_id", sa.String(length=26), nullable=False),
        # Record data (JSON)
        sa.Column("data", sa.JSON(), nullable=False),
        # Deletion metadata
        sa.Column("deleted_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_by", sa.String(length=26), nullable=True),
        sa.Column("note", sa.String(length=1000), nullable=True),
        # Constraints
        sa.PrimaryKeyConstraint("id", name=op.f("pk_archive")),
    )

    # Create indexes for common queries
    op.create_index(
        op.f("ix_archive_original_table"), "archive", ["original_table"], unique=False
    )
    op.create_index(
        op.f("ix_archive_original_id"), "archive", ["original_id"], unique=False
    )
    op.create_index(
        op.f("ix_archive_deleted_at"), "archive", ["deleted_at"], unique=False
    )


def downgrade() -> None:
    """Drop archive table."""
    op.drop_index(op.f("ix_archive_deleted_at"), table_name="archive")
    op.drop_index(op.f("ix_archive_original_id"), table_name="archive")
    op.drop_index(op.f("ix_archive_original_table"), table_name="archive")
    op.drop_table("archive")
