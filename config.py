import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("  ") or "sqlite:///" + os.path.join(
        basedir, "local.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
