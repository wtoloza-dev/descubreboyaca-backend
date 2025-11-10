"""Create dishes table.

Revision ID: 1d6caec41e69
Revises: 477b681fcc75
Create Date: 2025-10-26 11:20:16.947332

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "1d6caec41e69"
down_revision: str | None = "477b681fcc75"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create dishes table.

    This table stores dish/menu items for restaurants, including pricing,
    dietary information, flavor profiles, and availability status.
    """
    op.create_table(
        "dishes",
        # Audit fields (ULID + timestamps)
        sa.Column("id", sa.String(length=26), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("created_by", sa.String(length=26), nullable=True),
        sa.Column("updated_by", sa.String(length=26), nullable=True),
        # Foreign key to restaurant
        sa.Column("restaurant_id", sa.String(length=26), nullable=False),
        # Basic information
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=2000), nullable=True),
        sa.Column("category", sa.String(length=50), nullable=False),
        # Pricing (using DECIMAL for precise monetary values)
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("original_price", sa.Numeric(precision=10, scale=2), nullable=True),
        # Availability
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default="true"),
        # Additional details
        sa.Column("preparation_time_minutes", sa.Integer(), nullable=True),
        sa.Column("serves", sa.Integer(), nullable=True),
        sa.Column("calories", sa.Integer(), nullable=True),
        # Media
        sa.Column("image_url", sa.String(length=500), nullable=True),
        # Dietary information (stored as JSON arrays)
        sa.Column(
            "dietary_restrictions", sa.JSON(), nullable=False, server_default="[]"
        ),
        sa.Column("ingredients", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("allergens", sa.JSON(), nullable=False, server_default="[]"),
        # Flavor profile (stored as JSON object)
        sa.Column("flavor_profile", sa.JSON(), nullable=False, server_default="{}"),
        # Display options
        sa.Column("is_featured", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        # Constraints
        sa.PrimaryKeyConstraint("id", name=op.f("pk_dishes")),
        sa.ForeignKeyConstraint(
            ["restaurant_id"],
            ["restaurants.id"],
            name=op.f("fk_dishes_restaurant_id_restaurants"),
            ondelete="CASCADE",
        ),
        sa.CheckConstraint(
            "price >= 0",
            name=op.f("ck_dishes_price_positive"),
        ),
        sa.CheckConstraint(
            "original_price IS NULL OR original_price >= 0",
            name=op.f("ck_dishes_original_price_positive"),
        ),
        sa.CheckConstraint(
            "preparation_time_minutes IS NULL OR (preparation_time_minutes >= 0 AND preparation_time_minutes <= 600)",
            name=op.f("ck_dishes_preparation_time_range"),
        ),
        sa.CheckConstraint(
            "serves IS NULL OR (serves >= 1 AND serves <= 50)",
            name=op.f("ck_dishes_serves_range"),
        ),
        sa.CheckConstraint(
            "calories IS NULL OR (calories >= 0 AND calories <= 10000)",
            name=op.f("ck_dishes_calories_range"),
        ),
        sa.CheckConstraint(
            "display_order >= 0",
            name=op.f("ck_dishes_display_order_positive"),
        ),
    )

    # Create indexes for common queries
    op.create_index(
        op.f("ix_dishes_restaurant_id"), "dishes", ["restaurant_id"], unique=False
    )
    op.create_index(op.f("ix_dishes_name"), "dishes", ["name"], unique=False)
    op.create_index(op.f("ix_dishes_category"), "dishes", ["category"], unique=False)
    op.create_index(
        op.f("ix_dishes_is_available"), "dishes", ["is_available"], unique=False
    )
    op.create_index(
        op.f("ix_dishes_is_featured"), "dishes", ["is_featured"], unique=False
    )
    op.create_index(
        op.f("ix_dishes_display_order"), "dishes", ["display_order"], unique=False
    )


def downgrade() -> None:
    """Drop dishes table."""
    op.drop_index(op.f("ix_dishes_display_order"), table_name="dishes")
    op.drop_index(op.f("ix_dishes_is_featured"), table_name="dishes")
    op.drop_index(op.f("ix_dishes_is_available"), table_name="dishes")
    op.drop_index(op.f("ix_dishes_category"), table_name="dishes")
    op.drop_index(op.f("ix_dishes_name"), table_name="dishes")
    op.drop_index(op.f("ix_dishes_restaurant_id"), table_name="dishes")
    op.drop_table("dishes")
