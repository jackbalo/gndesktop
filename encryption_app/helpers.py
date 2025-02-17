from datetime import datetime
from flask import redirect, render_template, url_for, flash, current_app
from flask_login import current_user
from functools import wraps
from encryption_app.models import db, AuditLogs




def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def password_set(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("main.login"))
    
        if not current_user.password_set:
            flash("Please set a Password to continue")
            return redirect(url_for("main.add_password"))
        
        return f(*args, **kwargs)

    return decorated_function

def email_confirmed(f):
    """
    Decorate routes to require verification.
    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("main.login"))
    
        if not current_user.confirmed:
            flash("Account not verified!!")
            return redirect(url_for("main.otp_verification"))
        
        return f(*args, **kwargs)

    return decorated_function


#log users action
def log(action):
    try:
        user_log = AuditLogs(user_id=current_user.id, action=action, timestamp=datetime.now())
        db.session.add(user_log)
        db.session.commit()
    except Exception as e:
        raise


#convert to python date.
def date_convert(date):
    return datetime.strptime(date, '%Y-%m-%d').date()

