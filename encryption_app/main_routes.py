import requests 


from flask import flash, redirect, render_template, request, session, abort, Blueprint, url_for
from flask_login import current_user, login_required
from encryption_app.encoding import encrypt_text
from encryption_app.decoding import decrypt_text
from encryption_app.models import Activities, db
from  encryption_app.helpers import password_set, email_confirmed

main = Blueprint('main',__name__)


@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    return render_template("index.html")


@main.route("/home")
@login_required
@password_set
@email_confirmed
def home():
    user_activities = Activities.query.filter_by(user_id=current_user.id).all()
    formatted_user_activities = [
        {
            "date": activity.date.strftime("%Y-%m-%d %H:%M:%S"),
            "description": activity.description
        }
        for activity in user_activities
    ]
    return render_template("home.html", user=current_user, formatted_user_activities=formatted_user_activities)


@main.route("/profile")
@login_required
@password_set
def profile():
    return render_template("profile.html", user=current_user)


@main.route('/encrypt', methods=['GET', 'POST'])
@login_required
@password_set
@email_confirmed
def encrypt():
    encrypted_text = ''
    num_groups = 0
    if request.method == 'POST':
        # Ensure CSRF token is included in the form
        if not request.form.get('csrf_token'):
            abort(400, description="CSRF token missing")
        plaintext = request.form.get('plaintext', '').strip()
        key = request.form.get('key', '').strip()
        
        if not plaintext or not key:
            encrypted_text = "Input cannot be empty."
        else:
            encrypted_text, num_groups = encrypt_text(plaintext, key)
            # Log activity
            activity = Activities(user_id=current_user.id, description=f"Encrypted text with key '{key}'")
            db.session.add(activity)
            db.session.commit()
    
    return render_template('encrypt.html', encrypted_text=encrypted_text, num_groups=num_groups)


@main.route('/decrypt', methods=['GET', 'POST'])
@login_required
@password_set
@email_confirmed
def decrypt():
    decrypted_text = ''
    if request.method == 'POST':
        # Ensure CSRF token is included in the form
        if not request.form.get('csrf_token'):
            abort(400, description="CSRF token missing")
        encrypted_text = request.form.get('encrypted_text', '').strip()
        key = request.form.get('key', '').strip()
        
        if not encrypted_text or not key:
            decrypted_text = "Input cannot be empty."
        else:
            decrypted_text = decrypt_text(key, encrypted_text)
            # Log activity
            activity = Activities(user_id=current_user.id, description=f"Decrypted text with key '{key}'")
            db.session.add(activity)
            db.session.commit()
    
    return render_template('decrypt.html', decrypted_text=decrypted_text)


@main.route("/history")
@login_required
@password_set
@email_confirmed
def history():
    user_activities = Activities.query.filter_by(user_id=current_user.id).order_by(Activities.date.desc()).all()
    return render_template("history.html", user_activities=user_activities)
