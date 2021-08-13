from flask import Flask, request, jsonify

from server.models import Vote, Client
from datetime import datetime
from werkzeug.security import check_password_hash
from config import Config
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    app.config["SECRET_KEY"] = "secret key here"
    db.init_app(app)

    @app.route("/")
    def index():
        return "ok"

    @app.route("/feedback", methods=["POST"])
    def add_feedback():
        if not request.json or not "upvote" in request.json:
            return (jsonify({"error": "wrong_request"}), 400)

        if not "client" in request.json or not "token" in request.json:
            return (jsonify({"error": "not_authorised"}), 403)

        c = Client.query.filter_by(client=request.json["client"]).first()
        if c is None or not check_password_hash(c.token, request.json["token"]):
            return (jsonify({"error": "not_authorised"}), 403)
        v = Vote(
            client_id=c.client_id, upvote=request.json["upvote"], created=datetime.now()
        )
        db.session.add(v)
        db.session.commit()
        return jsonify({"created": "ok"})

    return app
