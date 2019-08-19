"""create entity_instances table

Revision ID: 0d2fdb4f68ee
Revises: dd84cb86e4c5
Create Date: 2019-08-19 04:43:49.474125

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "0d2fdb4f68ee"
down_revision = "dd84cb86e4c5"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "entity_instances",
        sa.Column(
            "id", UUID(), primary_key=True, server_default=sa.text("uuid_generate_v4()")
        ),
        sa.Column("entity_id", UUID(), sa.ForeignKey("entities.id")),
        sa.Column("moniker", sa.Text),
        sa.Column("zone", sa.Text),
        sa.Column("tick_time", sa.Numeric()),
        sa.Column("tick_variance", sa.Numeric()),
    )


def downgrade():
    op.drop_table("entity_instances")
