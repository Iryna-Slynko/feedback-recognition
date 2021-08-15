"""admin_user

Revision ID: 74218a1b3732
Revises: c37edd430cda
Create Date: 2021-06-29 00:21:38.881921

"""
from server.models import User
from server import db


# revision identifiers, used by Alembic.
revision = "74218a1b3732"
down_revision = "c37edd430cda"
branch_labels = None
depends_on = None


def upgrade():
    u = User(username="admin", role="admin")
    u.set_password("secret")
    db.session.add(u)
    db.session.commit()


def downgrade():
    pass
