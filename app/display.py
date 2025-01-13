from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import hashlib
import os
import re
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages and session management

# Configuration
UPLOAD_FOLDER = 'var/www/html/gndec_display/app/static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}
MAX_CONTENT_LENGTH = 15 * 1024 * 1024  # 15 MB max file size
HASHED_PASSWORD = "3312b14b1a872fb6997b371d4c880f1c"  # MD5 hash of "password"
SESSION_EXPIRATION_TIME = 5 * 60  # 5 minutes in seconds

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_input(input_string):
    # Remove potentially dangerous characters
    return re.sub(r'[<>\"\'%;()&+]', '', input_string)

def is_session_expired():
    """Check if the session has expired."""
    login_time = session.get('login_time')
    if not login_time or (time.time() - login_time > SESSION_EXPIRATION_TIME):
        return True
    return False

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/display', methods=['GET'])
def display_index():
    return app.send_static_file('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = sanitize_input(request.form['username'])
    password = sanitize_input(request.form['password'])
    hashed_input_password = hashlib.md5(password.encode()).hexdigest()

    if username == 'admin' and hashed_input_password == HASHED_PASSWORD:
        session['logged_in'] = True
        session['login_time'] = time.time()  # Store the login time in the session
        return redirect(url_for('upload_page'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('login_page'))

@app.route('/upload')
def upload_page():
    if 'logged_in' not in session or not session['logged_in'] or is_session_expired():
        session.clear()  # Clear session on expiration or unauthorized access
        flash('Your session has expired. Please log in again.', 'error')
        return redirect(url_for('login_page'))
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'logged_in' not in session or not session['logged_in'] or is_session_expired():
        session.clear()
        flash('Your session has expired. Please log in again.', 'error')
        return redirect(url_for('login_page'))
    
    try:
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('upload_page'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('upload_page'))
        
        if file and allowed_file(file.filename):
            # Remove all existing files in the upload folder
            for existing_file in os.listdir(app.config['UPLOAD_FOLDER']):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], existing_file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

            # Save the new file with a standardized name
            ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
            new_filename = f"gndec.{ext}"
            new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(new_file_path)

            flash('File uploaded successfully!', 'success')
            return redirect(url_for('upload_page'))
        else:
            flash('Unsupported file type', 'error')
            return redirect(url_for('upload_page'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('upload_page'))
    
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect('/')  # Redirect to the login page

    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(413)
def file_too_large(e):
    flash('File is too large. Maximum allowed size is 15 MB.', 'error')
    return redirect(url_for('upload_page'))

@app.route('/file', methods=['GET'])
def get_file():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    allowed_extensions = {'pdf', 'png', 'gif', 'jpg', 'jpeg', 'mp4'}
    for file in files:
        if file.split('.')[-1].lower() in allowed_extensions:
            return jsonify({'filename': file})
    return jsonify({'error': 'No valid file found'}), 404

@app.route('/static/uploads/<path:filename>')
def uploaded_file(filename):
    if allowed_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return "Unauthorized access", 403
    
import os
from flask import jsonify

@app.route('/latest-upload-timestamp')
def latest_upload_timestamp():
    uploads_dir = os.path.join(app.static_folder, 'uploads')
    try:
        # Get the latest modified file in the directory
        latest_file = max(
            (os.path.join(uploads_dir, f) for f in os.listdir(uploads_dir)),
            key=os.path.getmtime
        )
        latest_timestamp = os.path.getmtime(latest_file)
        return jsonify({'timestamp': latest_timestamp})
    except ValueError:
        # If the directory is empty
        return jsonify({'timestamp': None})

if __name__ == '__main__':
    app.run(debug=False)