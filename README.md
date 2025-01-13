# GNDEC Display Application

A web-based application designed to simplify **File uploads**, **Display functionality**, and to **Remotely Control Displays** for GNDEC. This project uses Python and Flask to deliver a lightweight, efficient solution.

---

## 📜 Application Description

The **GNDEC Display Application** is a Flask-based web application that provides a streamlined interface for managing file uploads, displaying dynamic content, and remote control. It is built to be modular and scalable.

---

## ✨ Features

- **Remote Control**:
  - Users can control display from anywhere in the world with provided login credentials from admin.
- **File Uploads**:
  - Users can upload files effortlessly, with robust handling of file types and sizes.
- **Dynamic Content Display**:
  - Displays user-uploaded files dynamically.
- **Error Handling**:
  - Custom error pages (e.g., 404 errors) for better user experience.
- **Static Resource Management**:
  - Serves static files (like images, stylesheets) efficiently.
- **Extensible Architecture**:
  - Modular design for future enhancements and integrations.

---

## 🛠️ Setup Instructions

Follow these steps to set up the application:

### 1. Clone the Repository
```bash
git clone https://github.com/Pawandadra/gndec_display.git
cd gndec_display
```
  - Ask for token at [pawankumark3610@gmail.com](mailto:pawankumark3610@gmail.com)
### 2. Create a Virtual Environment
  - Set up a virtual environment to isolate dependencies
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
  - Install the required Python libraries using pip:
```bash
pip install -r requirements.txt
```
### 4. Configure the Application
  - Ensure the UPLOAD_FOLDER and static directories have the proper permissions:
```bash
chmod -R 755 app/static
```
 - If necessary, adjust configuration settings in app/display.py or wsgi.py.

### 5. Run the Application Locally
 - Start the Flask development server:
```bash
python app/display.py
```
 - Visit http://127.0.0.1:5000 in your browser to see the application in action.

### Deploy to Production
 - For production, set up the application using Apache with mod_wsgi:
   - Install Apache on server.
   - Store application directory in /var/www/html
   - Create configuration file by
```bash
sudo nano /etc/apache2/sites-avaliable/gndec_display.conf
```
   - Your Configuration file should be like this
```bash
<VirtualHost *:80>
    ServerName <your-server-address>
    ServerAlias <put-additional-address-if-any>
    ServerAdmin admin@your-server-address

    DocumentRoot /var/www/html/gndec_display/
    WSGIDaemonProcess gndec_display python-home=/var/www/html/gndec_display/ven>
    WSGIScriptAlias / /var/www/html/gndec_display/wsgi.py

    <Directory /var/www/html/gndec_display/>
        Require all granted
    </Directory>

    Alias /static /var/www/html/gndec_display/app/static
    <Directory /var/www/html/gndec_display/app/static>
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/gndec_display_error.log
    CustomLog ${APACHE_LOG_DIR}/gndec_display_access.log combined
</VirtualHost>
```
   - test configuration by sudo apachectl configtest
   - Restart the Apache server:
```bash
sudo systemctl restart apache2
```

### Directory Structure
```bash
gndec_display/
│
├── app/
│   ├── static/               
│   │   └── uploads/          # Uploaded files
│   ├── templates/            # HTML templates
│   │   ├── 404.html          # Custom 404 error page
│   │   ├── login.html        # Login page
│   │   └── upload.html       # Upload page
│   └── display.py            # Core application logic
│
├── requirements.txt          # Python dependencies
├── wsgi.py                   # WSGI entry point
└── README.md                 # Project documentation
```