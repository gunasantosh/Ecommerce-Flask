from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()

db_user = "root"
db_password = "gtroot"
db_host = "localhost"
db_name = "rogold"


db = SQLAlchemy()
oauth = OAuth()
migrate = Migrate()


def create_app():
    app = Flask("__main__")
    app.config.from_object(Config)
    app.template_folder = "website/templates"
    app.static_folder = "website/static"

    db.init_app(app)
    oauth.init_app(app)
    migrate.init_app(app, db)

    print(os.getenv("client_id"))
    # Registering OAuth provider
    google = oauth.register(
        name="google",
        client_id=os.getenv("client_id"),
        client_secret=os.getenv("client_secret"),
        authorize_params=None,
        access_token_params=None,
        refresh_token_url="https://oauth2.googleapis.com/token",
        redirect_uri="http://localhost:5000/auth/callback",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid profile email"},
    )

    # Importing Blueprints
    from .views.home import home_bp
    from .views.admin import admin_bp
    from .views.auth import auth_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    with app.app_context():
        db.create_all()

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html")

    return app
