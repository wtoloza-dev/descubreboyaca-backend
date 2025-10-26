"""Create restaurants table.

Revision ID: d6e1a4f9747b
Revises: d91d67323aac
Create Date: 2025-10-21 09:18:56.988650

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "d6e1a4f9747b"
down_revision: str | None = "d91d67323aac"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create restaurants table.

    This table stores restaurant information for the Descubre Boyacá platform,
    including location data, contact info, cuisine types, and features.
    """
    op.create_table(
        "restaurants",
        # Audit fields (ULID + timestamps)
        sa.Column("id", sa.String(length=26), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("created_by", sa.String(length=26), nullable=True),
        sa.Column("updated_by", sa.String(length=26), nullable=True),
        # Basic information
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=True),
        # Address components
        sa.Column("address", sa.String(length=500), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column(
            "state", sa.String(length=100), nullable=False, server_default="Boyacá"
        ),
        sa.Column("postal_code", sa.String(length=20), nullable=True),
        sa.Column(
            "country", sa.String(length=100), nullable=False, server_default="Colombia"
        ),
        # Contact information
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("website", sa.String(length=500), nullable=True),
        # JSON fields
        sa.Column("location", sa.JSON(), nullable=True),
        sa.Column("social_media", sa.JSON(), nullable=True),
        # Business classification and categorization
        sa.Column("establishment_types", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("cuisine_types", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("price_level", sa.Integer(), nullable=True),
        sa.Column("features", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("tags", sa.JSON(), nullable=False, server_default="[]"),
        # Constraints
        sa.PrimaryKeyConstraint("id", name=op.f("pk_restaurants")),
        sa.CheckConstraint(
            "price_level >= 1 AND price_level <= 4",
            name=op.f("ck_restaurants_price_level_range"),
        ),
    )

    # Create indexes for common queries
    op.create_index(op.f("ix_restaurants_name"), "restaurants", ["name"], unique=False)
    op.create_index(op.f("ix_restaurants_city"), "restaurants", ["city"], unique=False)


def downgrade() -> None:
    """Drop restaurants table."""
    op.drop_index(op.f("ix_restaurants_city"), table_name="restaurants")
    op.drop_index(op.f("ix_restaurants_name"), table_name="restaurants")
    op.drop_table("restaurants")
