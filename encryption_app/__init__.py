# This file is the entry point for the application. It creates the Flask app and registers the main blueprint.
from flask import Flask, session
from flask_session import Session
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf import CSRFProtect
from datetime import timedelta  # Add this import
#from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
from encryption_app.models import db, Users
from encryption_app.config import Config
from encryption_app.main_routes import main
from encryption_app.auth_routes import auth

oauth_client = OAuth()
mail = Mail()
csrf = CSRFProtect()
#migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Session(app)

    db.init_app(app)
    oauth_client.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    #migrate.init_app(app,)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.register"

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    oauth_client.register(
        name="myApp",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        client_kwargs={
            "scope": "openid profile email",
            # 'code_challenge_method': 'S256'  # enable PKCE
        },
        server_metadata_url=app.config["GOOGLE_META_URL"]
        
    )

    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    return app