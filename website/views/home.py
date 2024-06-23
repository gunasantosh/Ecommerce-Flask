from flask import Blueprint, render_template, session
import json


home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    user = session.get("user")
    return render_template(
        "home/index.html",
        session=user,
        pretty=json.dumps(user, indent=4),
    )
