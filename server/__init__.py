from flask import Flask
from . import db, auth, user, data, client


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key here'

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(data.bp)
    app.register_blueprint(client.bp)

    @app.route('/')
    def index():
        return 'Hello, World!'

    return app
