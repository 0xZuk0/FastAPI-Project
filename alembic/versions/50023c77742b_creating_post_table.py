"""Creating post table

Revision ID: 50023c77742b
Revises: 
Create Date: 2022-01-15 21:37:07.762952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50023c77742b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id", sa.Integer, nullable=False, primary_key=True), sa.Column("title", sa.String, nullable=False))
    pass


def downgrade():
    op.drop_table("posts")
    pass
