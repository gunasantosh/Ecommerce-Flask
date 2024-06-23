from flask import Blueprint, redirect, url_for, session, abort
from authlib.integrations.flask_client import OAuth
from website import oauth
import os

auth_bp = Blueprint("auth", __name__)

# This google instance will use the one defined in __init__.py
google = oauth.google


@auth_bp.route("/login")
def login():
    if "user" in session:
        abort(404)
    redirect_uri = url_for("auth.callback", _external=True)
    return google.authorize_redirect(redirect_uri)


@auth_bp.route("/callback")
def callback():
    token = google.authorize_access_token()
    session["user"] = token
    return redirect(url_for("home.index"))


@auth_bp.route("logout")
def logout():
    session.pop("user")
    return redirect(url_for("home.index"))
