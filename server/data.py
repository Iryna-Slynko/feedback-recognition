import functools

from flask import (
    Blueprint, flash, g, jsonify, make_response,
    redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from server.auth import login_required
from server.db import get_db

bp = Blueprint('data', __name__, url_prefix='/data')


@bp.route('/view.json')
@login_required
def view():
    data = get_db().execute(
        "SELECT client_id, created, upvote"
        "FROM data"
    ).fetchall()
    return make_response(jsonify(data), 200)

@bp.route('/')
@login_required
def index():
    return render_template("data/index.html")