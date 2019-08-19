"""create properties table

Revision ID: dd84cb86e4c5
Revises: 0cebd14ad2e2
Create Date: 2019-08-19 04:34:46.007282

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "dd84cb86e4c5"
down_revision = "0cebd14ad2e2"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "entity_properties",
        sa.Column(
            "id", UUID(), primary_key=True, server_default=sa.text("uuid_generate_v4()")
        ),
        sa.Column("entity_id", UUID(), sa.ForeignKey("entities.id")),
        sa.Column("property_type", sa.Text),
    )


def downgrade():
    op.drop_table("entity_properties")
