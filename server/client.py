from flask import Blueprint, flash, render_template, request
from server.auth import admin_required
from server import db
from secrets import token_urlsafe
from server.models import Client

bp = Blueprint("client", __name__, url_prefix="/client")


@bp.route("/new", methods=("GET", "POST"))
@admin_required
def create():
    if request.method == "POST":
        client_name = request.form.get("client_name")
        location_id = request.form.get("location_id")
        error = None
        if not client_name:
            error = "Please enter the client name"
        elif not location_id:
            error = "Please enter the location id"
        elif Client.query.filter_by(client=client_name).count() > 0:
            error = "Client already exists."
        if error is None:
            token = token_urlsafe(30)
            c = Client(client=client_name, location_id=location_id)
            c.set_token(token)
            db.session.add(c)
            db.session.commit()
            return render_template(
                "client/show.html",
                token=token,
                client_name=client_name,
                status="created",
            )

        flash(error)

    return render_template("client/new.html")


@bp.route("/")
@admin_required
def index():
    clients = Client.query.all()
    return render_template("client/index.html", clients=clients)


@bp.route("/<int:client_id>/update", methods=("GET", "POST"))
@admin_required
def update(client_id):
    c = Client.query.filter(Client.client_id == client_id).first()
    if request.method == "POST":
        location_id = request.form.get("location_id")
        client_name = request.form.get("client_name")
        error = None
        if not client_name:
            error = "Please enter the client name"
        elif not location_id:
            error = "Please enter the location id"
        elif (
            Client.query.filter(
                Client.client == client_name, Client.client_id != client_id
            ).count()
            > 0
        ):
            error = "Client already exists."
        if error is None:
            token = token_urlsafe(30)
            c.client = client_name
            c.location_id = location_id
            c.set_token(token)
            db.session.commit()
            return render_template(
                "client/show.html",
                token=token,
                client_name=client_name,
                status="updated",
            )

        flash(error)

    return render_template("client/edit.html", client=c)
