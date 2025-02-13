import pyotp
from flask_mail import Message
from flask import url_for, flash, current_app
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime
import secrets

from encryption_app.models import Users, db
from encryption_app.helpers import log


def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def send_reset_email(email, token):
    from encryption_app import mail
    try:
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        msg = Message('Password Reset Request', sender='gncipher@gmail.com', recipients=[email])
        msg.body = f'Please click the link to reset your password: {reset_url}'
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Error sending reset email: {e}")
        raise


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except:
        return False
    return email


def generate_potp_secret_key():
    return pyotp.random_base32()


def generate_otp_code(potp_secret_key):
    totp = pyotp.TOTP(potp_secret_key, interval=600)
    return totp.now()


def verify_otp_code(potp_secret_key, otp_code):
    totp = pyotp.TOTP(potp_secret_key, interval=600)
    return totp.verify(otp_code)


def generate_state_token():
    return secrets.token_urlsafe(16)


def send_otp_email(receipient_email, otp_code):
    from encryption_app import mail
    try:
        msg = Message(
            subject="Your One-Time Password (OTP). ",
            recipients=[receipient_email],
            body=f"Your OTP is: {otp_code}\nThis code is valid for 60 seconds."
        )
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Error sending OTP email: {e}")
        raise
    

def verification_email(user):
    if not user.totp_secret:
        user.totp_secret = generate_potp_secret_key()

    user.last_otp_sent = datetime.now()
    db.session.commit()
    
    otp = generate_otp_code(user.totp_secret)

    try:
        send_otp_email(user.email, otp)
        flash(f"Verification code sent to your email {user.email}.")
        log(f"otp_email_{(user.email)}")
    except Exception as e:
        flash(f"Failed to send OTP: {str(e)}!")
        log("otp_email_failure")
        current_app.logger.error(f"Error during OTP email verification: {e}")
