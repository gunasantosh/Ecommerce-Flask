from flask import Blueprint, redirect, url_for, session, abort
from authlib.integrations.flask_client import OAuth
from website import oauth, db
import os
from website.models import User


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
    try:
        token = google.authorize_access_token()
        if not token:
            print("Token not authorized")
            return redirect(url_for("home.index"))

        session["user"] = token
        print("Token received and set in session:", token)

        # Extract userinfo from the token
        user_data = token.get("userinfo")
        if not user_data:
            print("User info not found in token")
            return redirect(url_for("home.index"))

        session["userinfo"] = user_data
        print("User info set in session:", user_data)

        email = user_data["email"]
        name = user_data["name"]
        picture = user_data["picture"]

        print(f"User Data - Email: {email}, Name: {name}, Picture: {picture}")

        user = User.query.filter_by(email=email).first()
        if not user:
            new_user = User(email=email, name=name, picture=picture)
            db.session.add(new_user)
        else:
            user.name = name
            user.picture = picture

        try:
            db.session.commit()
            print("User data committed to the database")
        except Exception as e:
            print("Error committing to database:", e)

    except Exception as e:
        print("Error in callback route:", e)

    return redirect(url_for("home.index"))


@auth_bp.route("logout")
def logout():
    session.pop("user")
    return redirect(url_for("home.index"))
