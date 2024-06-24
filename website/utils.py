from functools import wraps
from flask import redirect, url_for, session


ADMIN_EMAILS = [
    "bakiincorp@gmail.com",
]


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("auth.login"))
        user_data = session.get("userinfo")
        if not user_data or user_data["email"] not in ADMIN_EMAILS:
            return redirect(url_for("home.index"))
        return f(*args, **kwargs)

    return decorated_function
