import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configure session to use filesystem (instead of signed cookies)
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'None'
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes

    SECRET_KEY = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")

    SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # list of google scopes - https://developers.google.com/identity/protocols/oauth2/scopes

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_SCOPE = os.getenv("GOOGLE_SCOPE")
    GOOGLE_META_URL = os.getenv("GOOGLE_META_URL")

    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 465
    MAIL_USERNAME =  os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD =  os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
