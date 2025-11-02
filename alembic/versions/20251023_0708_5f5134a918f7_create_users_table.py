"""Create users table.

Revision ID: 5f5134a918f7
Revises: d6e1a4f9747b
Create Date: 2025-10-23 07:08:32.996942

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "5f5134a918f7"
down_revision: str | None = "d6e1a4f9747b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create users table.

    This table stores user information for authentication and authorization,
    supporting both email/password and OAuth2 (Google, etc.) authentication.
    """
    op.create_table(
        "users",
        # Primary key (ULID)
        sa.Column("id", sa.String(length=26), nullable=False),
        # User information
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        # OAuth fields
        sa.Column(
            "auth_provider",
            sa.String(length=50),
            nullable=False,
            server_default="email",
        ),
        sa.Column("google_id", sa.String(length=255), nullable=True),
        sa.Column("profile_picture_url", sa.String(length=500), nullable=True),
        # Timestamps
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        # Audit fields (user tracking)
        sa.Column("created_by", sa.String(length=26), nullable=True),
        sa.Column("updated_by", sa.String(length=26), nullable=True),
        # Constraints
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )

    # Create indexes for common queries
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_google_id"), "users", ["google_id"], unique=False)


def downgrade() -> None:
    """Drop users table."""
    op.drop_index(op.f("ix_users_google_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
