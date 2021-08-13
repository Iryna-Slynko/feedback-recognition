"""vote_table

Revision ID: c37edd430cda
Revises: c88e0371ce34
Create Date: 2021-06-28 22:58:45.991920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c37edd430cda"
down_revision = "c88e0371ce34"
branch_labels = None
depends_on = None


def downgrade():
    op.drop_table("vote")


def upgrade():
    op.create_table(
        "vote",
        sa.Column("vote_id", sa.INTEGER(), nullable=True),
        sa.Column("client_id", sa.INTEGER(), nullable=False),
        sa.Column(
            "created",
            sa.TIMESTAMP(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("upvote", sa.BOOLEAN(), nullable=False),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["client.client_id"],
        ),
        sa.PrimaryKeyConstraint("vote_id"),
    )
