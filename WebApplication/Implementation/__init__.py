import os
from firebase.firebase import FirebaseAuthentication
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask import Flask
from flask_login import LoginManager, UserMixin
from firebase import firebase

app = Flask(__name__)  # Create flask application
app.config['SECRET_KEY'] = str(os.environ.get('FLASK_SECRET_KEY'))  # Set secret key
app.config['SQLALCHEMY_DATABASE_URI'] = str(os.environ.get('SQLITE_URL'))  # Set SQLite database url
firebase = firebase.FirebaseApplication(str(os.environ.get('FIREBASE_URL')))  # Connect to firebase
authentication = FirebaseAuthentication(str(os.environ.get('DATABASE_SECRET')),
                                        str(os.environ.get('APP_ACCOUNT')),
                                        extra={'uid': str(os.environ.get('USER_ID'))})  # Authenticate to firebase
firebase.authentication = authentication  # Initialize authentication
db = SQLAlchemy(app)  # Initialize SQLAlchemy for managing SQLite database
bcrypt = Bcrypt(app)  # Initialize Bcrypt module. Used for password hashing
login_manager = LoginManager()  # Create LoginManager instance
login_manager.init_app(app)  # Initialize LoginManager. Used for managing user authentication
csrf = CSRFProtect(app)  # Initialize CSRF protection


class Users(UserMixin, db.Model):
    # Create database table
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(50), unique=True, nullable=False)  # Username field
    password = db.Column(db.String(80), nullable=False)  # Password field
    admin_role = db.Column(db.Boolean,
                           default=False)  # Field for admin role. If it is set on TRUE, the corresponding account has admin rights


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


from Implementation.accounts import accounts
from Implementation.controls import controls
from Implementation.main import main

app.register_blueprint(accounts)  # Include accounts blueprint
app.register_blueprint(controls)  # Include controls blueprint
app.register_blueprint(main)  # Include main blueprint

if __name__ == "__main__":
    app.run(debug=True)  # Start application
