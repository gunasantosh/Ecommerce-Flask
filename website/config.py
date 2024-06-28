import os


class Config:
    SECRET_KEY = "gt"
    SQLALCHEMY_DATABASE_URI = "mysql://root:gtroot@localhost/rogold"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = os.getenv("client_id")
    GOOGLE_SECRET_KEY = os.getenv("client_secret")
    ADMIN_EMAILS = [
        "bakiincorp@gmail.com",
    ]
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "static/uploads"
    )
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
