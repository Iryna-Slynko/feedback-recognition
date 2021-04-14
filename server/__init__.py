from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key here'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import user
    app.register_blueprint(user.bp)

    from . import data
    app.register_blueprint(data.bp)

    @app.route('/')
    def index():
        return 'Hello, World!'

    return app
