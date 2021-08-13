"""user_table

Revision ID: c88e0371ce34
Revises: c1f12c0ad3ca
Create Date: 2021-06-28 22:58:39.816612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c88e0371ce34"
down_revision = "c1f12c0ad3ca"
branch_labels = None
depends_on = None


def downgrade():
    op.drop_table("user")


def upgrade():
    op.create_table(
        "user",
        sa.Column("user_id", sa.INTEGER(), nullable=True),
        sa.Column("username", sa.TEXT(), nullable=False),
        sa.Column("password_hash", sa.TEXT(), nullable=False),
        sa.Column("role", sa.TEXT(), server_default=sa.text("'user'"), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("username"),
    )
