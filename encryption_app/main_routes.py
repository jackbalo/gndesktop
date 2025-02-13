import requests 
import os
import shutil
from werkzeug.utils import secure_filename
from flask import flash, redirect, render_template, request, session, abort, Blueprint, url_for, current_app, send_file
from flask_login import current_user, login_required
from encryption_app.encrypt import encrypt_text
from encryption_app.decrypt import decrypt_text
from encryption_app.models import Activities, db
from encryption_app.file_helpers import copy_section, create_document, replace_section, delete_file, duplicate_document
from  encryption_app.helpers import password_set, email_confirmed
from encryption_app.file_helpers import allowed_doc_file, UPLOAD_DOCS_FOLDER

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
    document_path = None
    uploaded_file_path = None
    duplicate_file_path = None
    try:
        if request.method == 'POST':
            # Ensure CSRF token is included in the form
            if not request.form.get('csrf_token'):
                abort(400, description="CSRF token missing")
            
            # Handle file upload
            if 'file' in request.files:
                file = request.files['file']
                if file and allowed_doc_file(file.filename):
                    filename = secure_filename(file.filename)
                    uploaded_file_path = os.path.join(UPLOAD_DOCS_FOLDER, filename)
                    
                    # Ensure the directory exists
                    os.makedirs(UPLOAD_DOCS_FOLDER, exist_ok=True)
                    
                    file.save(uploaded_file_path)
                    
                    # Create a duplicate of the uploaded document
                    duplicate_file_path = duplicate_document(uploaded_file_path)
                    
                    plaintext = copy_section(duplicate_file_path)
                else:
                    plaintext = request.form.get('plaintext', '').strip()
            else:
                plaintext = request.form.get('plaintext', '').strip()
            
            key = request.form.get('key', '').strip()
            
            if not plaintext or not key:
                encrypted_text = "Input cannot be empty."
            elif len(key) != 12:
                encrypted_text = "Key must be exactly 12 characters long."
            else:
                encrypted_text, num_groups = encrypt_text(plaintext, key)
                # Log activity
                activity = Activities(user_id=current_user.id, description=f"Encrypted text with key '{key}'")
                db.session.add(activity)
                db.session.commit()
                
                # Create document for download
                if duplicate_file_path:
                    replace_section(duplicate_file_path, encrypted_text)
                    document_path = os.path.basename(duplicate_file_path)
                else:
                    document_path = create_document(encrypted_text)
        
        # Schedule file deletion after 10 minutes (600 seconds)
        if uploaded_file_path:
            delete_file(uploaded_file_path, 600)
        if duplicate_file_path:
            delete_file(duplicate_file_path, 600)
        if document_path:
            delete_file(os.path.join(UPLOAD_DOCS_FOLDER, document_path), 600)
    except Exception as e:
        current_app.logger.error(f"Error during encryption: {e}")
        flash("An error occurred during encryption. Please try again.", "danger")
    
    return render_template('encrypt.html', encrypted_text=encrypted_text, num_groups=num_groups, document_path=document_path)


@main.route('/decrypt', methods=['GET', 'POST'])
@login_required
@password_set
@email_confirmed
def decrypt():
    decrypted_text = ''
    document_path = None
    uploaded_file_path = None
    duplicate_file_path = None
    try:
        if request.method == 'POST':
            # Ensure CSRF token is included in the form
            if not request.form.get('csrf_token'):
                abort(400, description="CSRF token missing")
            
            # Handle file upload
            if 'file' in request.files:
                file = request.files['file']
                if file and allowed_doc_file(file.filename):
                    filename = secure_filename(file.filename)
                    uploaded_file_path = os.path.join(UPLOAD_DOCS_FOLDER, filename)
                    
                    # Ensure the directory exists
                    os.makedirs(UPLOAD_DOCS_FOLDER, exist_ok=True)
                    
                    file.save(uploaded_file_path)
                    
                    # Create a duplicate of the uploaded document
                    duplicate_file_path = duplicate_document(uploaded_file_path)
                    
                    encrypted_text = copy_section(duplicate_file_path)
                else:
                    encrypted_text = request.form.get('encrypted_text', '').strip()
            else:
                encrypted_text = request.form.get('encrypted_text', '').strip()
            
            key = request.form.get('key', '').strip()
            
            if not encrypted_text or not key:
                decrypted_text = "Input cannot be empty."
            else:
                decrypted_text = decrypt_text(encrypted_text, key)
                # Log activity
                activity = Activities(user_id=current_user.id, description=f"Decrypted text with key '{key}'")
                db.session.add(activity)
                db.session.commit()

                # Create document for download
                if duplicate_file_path:
                    replace_section(duplicate_file_path, decrypted_text)
                    document_path = os.path.basename(duplicate_file_path)
                else:
                    document_path = create_document(decrypted_text)

        # Schedule file deletion after 10 minutes (600 seconds)
        if uploaded_file_path:
            delete_file(uploaded_file_path, 600)
        if duplicate_file_path:
            delete_file(duplicate_file_path, 600)
        if document_path:
            delete_file(os.path.join(UPLOAD_DOCS_FOLDER, document_path), 600)
    except Exception as e:
        current_app.logger.error(f"Error during decryption: {e}")
        flash("An error occurred during decryption. Please try again.", "danger")
    
    return render_template('decrypt.html', decrypted_text=decrypted_text, document_path=document_path)


@main.route("/history")
@login_required
@password_set
@email_confirmed
def history():
    user_activities = Activities.query.filter_by(user_id=current_user.id).order_by(Activities.date.desc()).all()
    return render_template("history.html", user_activities=user_activities)


@main.route('/download/<filename>')
@login_required
def download_file(filename):
    file_path = os.path.join(UPLOAD_DOCS_FOLDER, filename)
    if os.path.exists(file_path):
        response = send_file(file_path, as_attachment=True)
        os.remove(file_path)  # Cleanup the file after sending it
        return response
    abort(404)


