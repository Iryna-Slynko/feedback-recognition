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
        client_name = request.form.get('client_name')
        location_id = request.form.get('location_id')
        db = get_db()
        error = None
        if not client_name:
            error = 'Please enter the client name'
        elif not location_id:
            error = 'Please enter the location id'
        elif (
            db.execute("SELECT client_id FROM client WHERE client = ?",
                       (client_name,)).fetchone()
            is not None
        ):
            error = 'Client already exists.'
        if error is None:
            token = token_urlsafe(30)
            db.execute(
                "INSERT INTO client (client, token, token_start, location_id) VALUES (?, ?, ?, ?)",
                (client_name, generate_password_hash(token), token[0:3], location_id),
            )
            db.commit()
            return render_template('client/show.html', token=token, client_name=client_name)

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

@bp.route('/<int:client_id>/update', methods=('GET', 'POST'))
@admin_required
def update(client_id):
    return render_template("client/edit.html")