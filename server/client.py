from flask import (
    Blueprint, flash, render_template, request
)
from werkzeug.security import generate_password_hash
from server.auth import admin_required
from server.db import get_db
from secrets import token_urlsafe

bp = Blueprint('client', __name__, url_prefix='/client')


@bp.route('/new', methods=('GET', 'POST'))
@admin_required
def create():
    if request.method == 'POST':
        client_name = request.form['client']
        location_id = request.form['location_id']
        db = get_db()
        error = None
        if (
            db.execute("SELECT id FROM client WHERE client = ?",
                       (client_name,)).fetchone()
            is not None
        ):
            error = 'User already exists.'
        if error is None:
            token = token_urlsafe(30)
            db.execute(
                "INSERT INTO client (client, token, token_start, location_id) VALUES (?, ?, ?)",
                (client_name, generate_password_hash(token), token[0:3], location_id),
            )
            db.commit()
            return redirect(url_for('user.index'))

        flash(error)

    return render_template('client/new.html')


@bp.route('/')
@admin_required
def index():
    clients = get_db().execute(
        "SELECT client_id, client, token_start, location_id"
        " FROM client"
    ).fetchall()
    return render_template("client/index.html", clients=clients)
