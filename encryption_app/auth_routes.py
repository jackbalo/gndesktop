import requests
import pyotp
from werkzeug.utils import secure_filename
import os

from flask import flash, redirect, render_template, request, session, abort, Blueprint, url_for
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message, Mail
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import func
from datetime import datetime
from encryption_app.models import  db, Users
from encryption_app.helpers import apology, log, password_set, email_confirmed
from encryption_app.email_helpers import verification_email, send_reset_email, generate_token, confirm_token, generate_potp_secret_key, verify_otp_code, generate_state_token
from encryption_app.file_helpers import UPLOAD_PICS_FOLDER, allowed_pic_file



auth = Blueprint('auth', __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    errors = {}
    if request.method == "POST":
        # Ensure CSRF token is included in the form
        if not request.form.get('csrf_token'):
            abort(400, description="CSRF token missing")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(password, method='pbkdf2:sha256:600000', salt_length=16)
            
        if not password or not email:
            errors = {"email": "Email is required", "password": "Password is required"}
            return render_template("register.html", errors=errors)
        
        if password != confirmation:
            errors = {"confirmation": "Passwords do not match"}
            return render_template("register.html", errors=errors)
        
        try:
            user = Users(username=username, hash=hash, email=email, password_set=True, totp_secret=generate_potp_secret_key())
            db.session.add(user)
            db.session.commit()

            user = Users.query.filter_by(email=email).first()
            if not user or not check_password_hash(user.hash,password):
                errors = {"email": "Invalid Username or Password"}
                return render_template("register.html", errors=errors)

            login_user(user)
            log("register")

        except ValueError:
            errors = {"username": "Username already exists"}
            return render_template("register.html", errors=errors)
        
        verification_email(current_user)
        return redirect(url_for("auth.otp_verification"))
    
    else:
        return render_template("register.html", errors=errors)
    

@auth.route("/otp_verification", methods=["GET", "POST"])
@login_required
@password_set
def otp_verification():
    errors = {}
    if request.method == "POST":
        if 'resend_otp' in request.form:
            time_last_otp_sent = None
            if current_user.last_otp_sent: 
                time_last_otp_sent = (datetime.now() - current_user.last_otp_sent).total_seconds()  
                if time_last_otp_sent and time_last_otp_sent < 60:
                    flash(f"Resend otp in {60 - int(time_last_otp_sent)} seconds!! ")
                else:
                    verification_email(current_user)
                return redirect(url_for("auth.otp_verification"))
            else:
                verification_email(current_user)
            return redirect(url_for("auth.otp_verification"))
        else:
            otp = request.form.get("otp")
            if not otp:
                errors = {"otp": "Please Enter OTP"}
                return render_template("otp_verification.html", errors=errors)
            
            if verify_otp_code(current_user.totp_secret, otp):
                current_user.confirmed = True
                current_user.confirmed_on = datetime.now()
                db.session.commit()
                flash("OTP verification successful! ")
                log("otp_verified")
                return redirect(url_for("main.home"))
            else: 
                errors = {"otp": "Invalid or expired OTP"}
                log("OTP_verification_failed!! ")
                return render_template("otp_verification.html", errors=errors)
            
    time_last_otp_sent = None
    if current_user.last_otp_sent: 
        time_last_otp_sent = (datetime.now() - current_user.last_otp_sent).total_seconds()
        countdown = max(0, int(60 - time_last_otp_sent)) if time_last_otp_sent else 60

    return render_template("otp_verification.html", user=current_user, countdown=countdown, errors=errors)


@auth.route("/add_password", methods=["GET", "POST"])
def add_password():
    """Register user"""
    errors = {}
    if current_user.password_set:
        flash("Already added Password")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not password or not confirmation:
            errors = {"password": "Password is required", "confirmation": "Confirmation is required"}
            return render_template("add_password.html", errors=errors)
        
        if password != confirmation:
            errors = {"confirmation": "Passwords do not match"}
            return render_template("add_password.html", errors=errors)
        
        current_user.hash = generate_password_hash(password, method='pbkdf2:sha256:600000', salt_length=16)
        current_user.password_set = True
        db.session.commit()

        log("google_register")

        if not current_user.confirmed:
            verification_email(current_user)
            return redirect(url_for("auth.otp_verification"))
    
    return render_template("add_password.html", user=current_user, errors=errors)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    errors = {}
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure CSRF token is included in the form
        if not request.form.get('csrf_token'):
            abort(400, description="CSRF token missing")
        # Ensure username was submitted
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            errors = {"email": "Email is required", "password": "Password is required"}
            return render_template("login.html", errors=errors)

        # Query database for username
        user = Users.query.filter_by(email=email).first()

        # Ensure username exists and password is correct
        if not user or not check_password_hash(user.hash, password):
            errors = {"email": "Invalid username and/or password"}
            return render_template("login.html", errors=errors)

        login_user(user)
        log("log_in")
        return redirect(url_for("main.home"))

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html", errors=errors)


@auth.route("/signin-google")
def googleCallback():
    from encryption_app import oauth_client
    # fetch access token and id token using authorization code
    try:
        state = request.args.get('state')
        if state != session.pop('oauth_state', None):
            raise ValueError("State mismatch")
        token = oauth_client.myApp.authorize_access_token()
        
        if not token:
            raise ValueError("Failed to fetch token")

        email = token["userinfo"]["email"]
        name = token["userinfo"]["name"]
        google_id = token["userinfo"]["sub"]
       
        user = Users.query.filter_by(email=email).first()
        if not user:
            user = Users(username=name, email=email, google_id=google_id, totp_secret=generate_potp_secret_key(), last_otp_sent=datetime.now())
            db.session.add(user)
            db.session.commit()

        login_user(user)

        if not user.password_set:
            return redirect(url_for("auth.add_password"))
        
        if not user.confirmed:
            verification_email(user)  # Use 'user' instead of 'current_user'
            return redirect(url_for("auth.otp_verification"))
                
        log(f"google_login_{name}")
        return redirect(url_for("main.home"))

    except ValueError as e:
        log(f"Google login error: {str(e)}")
        return apology("Unauthorized login", 403)

@auth.route("/google-login")
def googleLogin():
    from encryption_app import oauth_client
    if current_user.is_authenticated:
        abort(404)
    state = generate_state_token()  # Generate a state token
    session['oauth_state'] = state  # Store the state token in the session
    return oauth_client.myApp.authorize_redirect(redirect_uri=url_for("auth.googleCallback", _external=True), state=state)


@auth.route("/update_profile/<int:id>", methods=["GET", "POST"])
@login_required
@password_set
@email_confirmed
def update_profile(id):
    '''Update user profile'''
    user = Users.query.get_or_404(id)
    if request.method == "POST":
        # Ensure CSRF token is included in the form
        if not request.form.get('csrf_token'):
            abort(400, description="CSRF token missing")
        current_user.username = request.form.get("username") or current_user.username
        current_user.email = request.form.get("email") or current_user.email
        password = request.form.get("password")

        if not password or not check_password_hash(current_user.hash, password):
            flash("Enter Valid password")
            return redirect(url_for('auth.update_profile', id=id))
        
        db.session.commit()
        log("profile_update")
        flash("Profile updated successfully")
        return redirect(url_for('main.profile'))
    
    return render_template("update_profile.html", user=user)


@auth.route("/logout")
@login_required
def logout():
    """Log user out"""
    #Add to logs
    log("log out")
    logout_user()
    flash("You have successfully logged out")
    return redirect(url_for("main.index"))


@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = Users.query.filter_by(email=email).first()
        if user:
            token = generate_token(user.email)
            send_reset_email(user.email, token)
            flash('A password reset link has been sent to your email.', 'success')
        else:
            flash('Email address not found.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    return render_template('forgot_password.html')


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = Users.query.filter_by(email=email).first()
        if user:
            token = generate_token(user.email)
            send_reset_email(user.email, token)
            flash('A link has been sent to your email.', 'success')
        else:
            flash('Email address not found.', 'danger')
        return redirect(url_for('auth.change_password'))
    
    return render_template('change_password.html')


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    errors = {}
    try:
        email = confirm_token(token)
    except:
        flash('The reset link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        # Ensure CSRF token is included in the form
        if not request.form.get('csrf_token'):
            abort(400, description="CSRF token missing")
        password = request.form.get('new_password')
        confirmation = request.form.get('confirmation')
        if not password or not confirmation:
            errors = {"new_password": "Password is required", "confirmation": "Confirmation is required"}
            return render_template('reset_password.html', token=token, errors=errors)
        if password == confirmation:
            user = Users.query.filter_by(email=email).first()
            user.hash = generate_password_hash(password)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            if current_user.is_authenticated:
                return redirect(url_for('main.profile'))
            else:
                return redirect(url_for('auth.login'))
        else:
            errors = {"confirmation": "Passwords do not match"}
            return render_template('reset_password.html', token=token, errors=errors)
    return render_template('reset_password.html', token=token, errors=errors)


@auth.route('/upload_profile_pic', methods=['POST'])
@login_required
def upload_profile_pic():
    if 'profile_pic' not in request.files:
        flash('No file part')
        return redirect(url_for('main.profile'))
    
    file = request.files['profile_pic']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('main.profile'))
    
    if file and allowed_pic_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_PICS_FOLDER, filename))
        current_user.profile_pic = filename
        db.session.commit()
        flash('Profile picture updated successfully')
        return redirect(url_for('main.profile'))
    
    flash('Allowed file types are png, jpg, jpeg, gif')
    return redirect(url_for('main.profile'))

