from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.security import generate_password_hash
from server.auth import admin_required
from server import db

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/new', methods=('GET', 'POST'))
@admin_required
def create():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form['role']
        db = get_db()
        error = None
        if not username:
            error = 'Username is not set'
        elif not password:
            error = 'Password is not set'
        elif role != 'user' or role != 'admin':
            error = 'Incorrect role'
        elif (
            db.execute("SELECT id FROM user WHERE username = ?",
                       (username,)).fetchone()
            is not None
        ):
            error = 'User already exists.'
        if error is None:
            db.execute(
                "INSERT INTO user (username, password, role) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), role),
            )
            db.commit()
            return redirect(url_for('user.index'))

        flash(error)

    return render_template('user/new.html')


@bp.route('/')
@admin_required
def index():
    users = get_db().execute(
        "SELECT user_id, username, role"
        " FROM user"
    ).fetchall()
    return render_template("user/index.html", users=users)
