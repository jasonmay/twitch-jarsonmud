"""create entity table

Revision ID: 0cebd14ad2e2
Revises: 
Create Date: 2019-08-19 03:49:03.333699

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = "0cebd14ad2e2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "entities",
        sa.Column(
            "id", UUID(), primary_key=True, server_default=sa.text("uuid_generate_v4()")
        ),
        sa.Column("label", sa.Text),
    )


def downgrade():
    op.drop_table("entities")
