import functools

from flask import request, redirect, url_for, flash, render_template, session, Blueprint, g
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash

from web_server.models import Users, db

bp = Blueprint("auth", __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = Users.query.filter_by(id=user_id).first()


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        error = None

        if not username:
            error = "Username is required."
        elif not email:
            error = "Email is required"
        elif not password:
            error = "Password is required"

        if error is None:
            try:
                hashed_password = generate_password_hash(password)
                user = Users(username=username, email=email, hashed_password=hashed_password)
                db.session.add(user)
                db.session.commit()

            except exc.IntegrityError:
                error = f"Email or username is already registered"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        user = Users.query.filter_by(username=username).first()
        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user.hashed_password, password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index"))
        flash(error)
    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
