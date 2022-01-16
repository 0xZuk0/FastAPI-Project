"""add content column into posts table

Revision ID: f40c413cd01a
Revises: 50023c77742b
Create Date: 2022-01-15 21:44:42.187223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f40c413cd01a'
down_revision = '50023c77742b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
