from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.security import generate_password_hash
from server.auth import admin_required
from server import db
from server.models import User

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/new', methods=('GET', 'POST'))
@admin_required
def create():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form['role']
        error = None
        if not username:
            error = 'Username is not set'
        elif not password:
            error = 'Password is not set'
        elif role != 'user' and role != 'admin':
            error = 'Incorrect role'
        elif (
            User.query.filter_by(username=username).first() is not None
        ):
            error = 'User already exists.'
        if error is None:
            u = User(username=username, role=role)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('user.index'))

        flash(error)

    return render_template('user/new.html')


@bp.route('/')
@admin_required
def index():
    users = User.query.all()
    return render_template("user/index.html", users=users)
