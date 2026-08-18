"""
create spots table

Revision ID: 20cc2e7635bc
Revises: d818bab27c62
Create Date: 2026-08-18

"""
from typing import Sequence, Union

import sqlalchemy as sa
import geoalchemy2
from alembic import op

revision: str = "20cc2e7635bc"
down_revision: Union[str, Sequence[str], None] = "d818bab27c62"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "spots",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        # geoalchemy2.types.Geography: stessa colonna del modello Spot.
        # Solo la creazione manuale controlla il tipo e l'SRID.
        sa.Column(
            "location",
            geoalchemy2.types.Geography(geometry_type="POINT", srid=4326, spatial_index=False),
            nullable=False,
        ),
        sa.Column("radius", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    # Indice spaziale GIST: le query su location (ST_DWithin ecc.)
    # senza indice farebbero full scan.
    op.create_index(
        "idx_spots_location",
        "spots",
        ["location"],
        unique=False,
        postgresql_using="gist",
    )


def downgrade() -> None:
    op.drop_index("idx_spots_location", table_name="spots", postgresql_using="gist")
    op.drop_table("spots")