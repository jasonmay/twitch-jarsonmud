"""add property_name to entity_properties table

Revision ID: 09869789a71a
Revises: 5332ad548c68
Create Date: 2019-08-20 03:38:14.308106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "09869789a71a"
down_revision = "5332ad548c68"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("entity_properties", sa.Column("property_name", sa.String()))


def downgrade():
    op.drop_column("entity_properties", "property_name")
