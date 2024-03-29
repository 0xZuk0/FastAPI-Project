"""add users table

Revision ID: d28563328e70
Revises: f40c413cd01a
Create Date: 2022-01-15 21:49:47.320064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd28563328e70'
down_revision = 'f40c413cd01a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users", 
        sa.Column("id", sa.Integer(), nullable=False), 
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )
    pass


def downgrade():
    op.drop_table("users")
    pass
