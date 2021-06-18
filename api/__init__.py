from flask import Flask
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import server.db as db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key here'

    db.init_app(app)

    @app.route('/')
    def index():
        return 'ok'

    return app
