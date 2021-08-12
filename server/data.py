import functools

from flask import (
    Blueprint, flash, g, jsonify, make_response,
    redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from server.auth import login_required
from server import db
from server.models import VoteDaily

bp = Blueprint('data', __name__, url_prefix='/data')


@bp.route('/view.json')
@login_required
def view():
    location_id = 45
    data = VoteDaily.query.filter_by(location_id=location_id).all()
    return make_response(jsonify([d.serialize for d in data]), 200)


@bp.route('/')
@login_required
def index():
    return render_template("data/index.html")
