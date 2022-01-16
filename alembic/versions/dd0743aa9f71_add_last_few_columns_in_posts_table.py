"""add last few columns in posts table

Revision ID: dd0743aa9f71
Revises: e74bd776e54b
Create Date: 2022-01-15 22:12:53.082391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd0743aa9f71'
down_revision = 'e74bd776e54b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean, nullable=False, server_default="TRUE")
    )
    op.add_column(
        "posts",
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False)
    )
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
