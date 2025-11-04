"""Create favorites table.

Revision ID: 2f8a3c9b4e5d
Revises: 1d6caec41e69
Create Date: 2025-10-26 15:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "2f8a3c9b4e5d"
down_revision: str | None = "1d6caec41e69"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create favorites table.

    This table implements a polymorphic favorites system that can store
    favorites for any type of entity (restaurants, dishes, events, places, activities).
    This design is scalable - adding new entity types only requires updating
    the EntityType enum, no schema changes needed.
    """
    op.create_table(
        "favorites",
        # Primary key (ULID)
        sa.Column("id", sa.String(length=26), nullable=False),
        # Foreign key to users
        sa.Column(
            "user_id",
            sa.String(length=26),
            nullable=False,
        ),
        # Polymorphic fields for any entity type
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.String(length=26), nullable=False),
        # Timestamps
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        # Constraints
        sa.PrimaryKeyConstraint("id", name=op.f("pk_favorites")),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_favorites_user_id_users"),
            ondelete="CASCADE",
        ),
        # Unique constraint: one user cannot favorite the same entity twice
        sa.UniqueConstraint(
            "user_id",
            "entity_type",
            "entity_id",
            name=op.f("uq_favorites_user_entity"),
        ),
    )

    # Create indexes for efficient queries
    op.create_index(
        op.f("ix_favorites_user_id"), "favorites", ["user_id"], unique=False
    )
    op.create_index(
        op.f("ix_favorites_entity_type"), "favorites", ["entity_type"], unique=False
    )
    op.create_index(
        op.f("ix_favorites_entity_id"), "favorites", ["entity_id"], unique=False
    )
    op.create_index(
        op.f("ix_favorites_created_at"), "favorites", ["created_at"], unique=False
    )
    # Compound index for listing favorites by user and type
    op.create_index(
        op.f("ix_favorites_user_type"),
        "favorites",
        ["user_id", "entity_type"],
        unique=False,
    )
    # Compound index for counting favorites on an entity
    op.create_index(
        op.f("ix_favorites_entity"),
        "favorites",
        ["entity_type", "entity_id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop favorites table."""
    op.drop_index(op.f("ix_favorites_entity"), table_name="favorites")
    op.drop_index(op.f("ix_favorites_user_type"), table_name="favorites")
    op.drop_index(op.f("ix_favorites_created_at"), table_name="favorites")
    op.drop_index(op.f("ix_favorites_entity_id"), table_name="favorites")
    op.drop_index(op.f("ix_favorites_entity_type"), table_name="favorites")
    op.drop_index(op.f("ix_favorites_user_id"), table_name="favorites")
    op.drop_table("favorites")
