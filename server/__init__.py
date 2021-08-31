from config import Config
from flask import redirect, url_for, Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from server import auth, client, data, user

app.config["SECRET_KEY"] = "secret key here"
db.init_app(app)
app.register_blueprint(auth.bp)

app.register_blueprint(user.bp)
app.register_blueprint(data.bp)
app.register_blueprint(client.bp)


@app.route("/")
def index():
    return redirect(url_for("data.index"))
