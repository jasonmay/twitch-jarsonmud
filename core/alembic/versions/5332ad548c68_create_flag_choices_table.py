"""create flag_choices table

Revision ID: 5332ad548c68
Revises: 06ed1a015362
Create Date: 2019-08-19 05:05:26.540488

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "5332ad548c68"
down_revision = "06ed1a015362"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "entity_property_flag_choices",
        sa.Column(
            "id", UUID(), primary_key=True, server_default=sa.text("uuid_generate_v4()")
        ),
        sa.Column("entity_property_id", UUID(), sa.ForeignKey("entity_properties.id")),
        sa.Column("flag_value", sa.Text()),
    )


def downgrade():
    op.drop_table("entity_property_flag_choices")
