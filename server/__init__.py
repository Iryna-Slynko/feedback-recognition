from flask import Flask

from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from server import auth, user, data, client

app.config['SECRET_KEY'] = 'secret key here'
db.init_app(app)
app.register_blueprint(auth.bp)

app.register_blueprint(user.bp)
app.register_blueprint(data.bp)
app.register_blueprint(client.bp)

@app.route('/')
def index():
    return 'Hello, World!'

