"""votes_view

Revision ID: e989894011cc
Revises: 74218a1b3732
Create Date: 2021-07-25 22:48:56.612319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e989894011cc'
down_revision = '74218a1b3732'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE VIEW vote_daily AS 
        SELECT  SUM(CASE WHEN v.upvote THEN 1 ELSE 0 END) as upvotes, 
                SUM(CASE WHEN v.upvote THEN 0 ELSE 1 END) as downvotes,
                DATE(v.created) as 'date', c.location_id
                FROM vote v
                INNER JOIN client c on c.client_id = v.client_id
                GROUP BY 3, 4
    """)


def downgrade():
     op.execute("""
        DROP VIEW vote_daily
    """)
