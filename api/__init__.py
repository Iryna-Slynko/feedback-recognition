from flask import Flask, request, jsonify

import server.db as db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key here'

    db.init_app(app)

    @app.route('/')
    def index():
        return 'ok'

    @app.route('/feedback', methods=['POST'])
    def add_feedback():
        if not request.json or not 'upvote' in request.json:
           return (jsonify({"error": "wrong_request"}), 400)

        return jsonify({"created": "ok"})

    return app
