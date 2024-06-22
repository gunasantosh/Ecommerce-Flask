from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db_user = "root"
db_password = "gtroot"
db_host = "localhost"
db_name = "rogold"


db = SQLAlchemy()


def create_app():
    app = Flask("__main__")
    app.config["SECRET_KEY"] = "gt"
    app.template_folder = "website/templates"
    app.static_folder = "website/static"

    # Database Setup
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(
        db_user, db_password, db_host, db_name
    )
    app.config["SQLALCHEMY_TRACK_MOFIFICATIONS"] = False
    db.init_app(app)

    # Importing Blueprints
    from .views.home import home_bp
    from .views.admin import admin_bp
    from .views.auth import auth_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html")

    return app
