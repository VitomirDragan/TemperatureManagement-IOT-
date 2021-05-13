import os
from firebase.firebase import FirebaseAuthentication
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask import Flask
from flask_login import LoginManager, UserMixin
from firebase import firebase

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.environ.get('FLASK_SECRET_KEY'))
app.config['SQLALCHEMY_DATABASE_URI'] = str(os.environ.get('SQLITE_URL'))
firebase = firebase.FirebaseApplication(str(os.environ.get('FIREBASE_URL')))
authentication = FirebaseAuthentication(str(os.environ.get('DATABASE_SECRET')),
                                        str(os.environ.get('APP_ACCOUNT')),
                                        extra={'uid': str(os.environ.get('USER_ID'))})
firebase.authentication = authentication
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
csrf = CSRFProtect(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    admin_role = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


from Implementation.accounts import accounts
from Implementation.controls import controls
from Implementation.main import main

app.register_blueprint(accounts)
app.register_blueprint(controls)
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)

