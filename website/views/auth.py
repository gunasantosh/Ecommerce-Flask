from flask import Blueprint, session, redirect, render_template
from authlib.integrations.flask_client import OAuth


auth_bp = Blueprint("home", __name__)
oauth = OAuth()


@auth_bp.route("/login")
def login():
    # redirect_uri = url_for("auth", _external=True)
    # return oauth.google.authorize_redirect(redirect_uri)
    pass


@auth_bp.route("/auth")
def auth():
    token = oauth.google.authorize_access_token()
    session["user"] = token["userinfo"]
    return redirect("/")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")
