"""create entity_property_instances table

Revision ID: 06ed1a015362
Revises: 0d2fdb4f68ee
Create Date: 2019-08-19 04:57:51.795337

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "06ed1a015362"
down_revision = "0d2fdb4f68ee"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "entity_property_instances",
        sa.Column(
            "id", UUID(), primary_key=True, server_default=sa.text("uuid_generate_v4()")
        ),
        sa.Column("entity_instance_id", UUID(), sa.ForeignKey("entity_instances.id")),
        sa.Column("entity_property_id", UUID(), sa.ForeignKey("entity_properties.id")),
        sa.Column("value_uuid", UUID()),
        sa.Column("value_str", sa.Text()),
        sa.Column("value_int", sa.BigInteger()),
        sa.Column("value_numeric", sa.Numeric()),
        sa.Column("value_struct", sa.JSON()),
    )


def downgrade():
    op.drop_table("entity_property_instances")
