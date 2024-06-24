import os


class Config:
    SECRET_KEY = "gt"
    SQLALCHEMY_DATABASE_URI = "mysql://root:gtroot@localhost/rogold"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = os.getenv("client_id")
    GOOGLE_SECRET_KEY = os.getenv("client_secret")
