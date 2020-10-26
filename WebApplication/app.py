from flask import Flask, render_template, request, url_for, flash, redirect
from firebase import firebase
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

firebase = firebase.FirebaseApplication('https://temperaturemanagement-iot.firebaseio.com')

app = Flask(__name__)

app.config['SECRET_KEY'] = '\xcf\x89\xe9v\x81Xf\xa5\x17\x17\x118\xad\xf3V\xce\x06\xb4\xc1\xa5\xce\x15\x9f1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    admin_role = db.Column(db.Boolean, default=False)


@app.route('/room1', methods=['POST', 'GET'])
def room1():
    temp1 = firebase.get('CurrentTempRoom1', 'Value')
    temp2 = firebase.get('CurrentTempRoom2', 'Value')
    hum1 = firebase.get('HumidityRoom1', 'Value')
    hum2 = firebase.get('HumidityRoom2', 'Value')
    if request.method == 'POST':
        variable = request.form['content']
        firebase.put('DesiredTempRoom1', 'Value', int(variable))
        return render_template('controlPage.html', tempR1=temp1, tempR2=temp2, humR1=hum1, humR2=hum2)
    else:
        return render_template('controlPage.html', tempR1=temp1, tempR2=temp2, humR1=hum1, humR2=hum2)


@app.route('/room2', methods=['POST', 'GET'])
def room2():
    temp1 = firebase.get('CurrentTempRoom1', 'Value')
    temp2 = firebase.get('CurrentTempRoom2', 'Value')
    hum1 = firebase.get('HumidityRoom1', 'Value')
    hum2 = firebase.get('HumidityRoom2', 'Value')
    if request.method == 'POST':
        variable = request.form['content2']
        firebase.put('DesiredTempRoom2', 'Value', int(variable))
        return render_template('controlPage.html', tempR1=temp1, tempR2=temp2, humR1=hum1, humR2=hum2)
    else:
        return render_template('controlPage.html', tempR1=temp1, tempR2=temp2, humR1=hum1, humR2=hum2)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_to_login = Users.query.filter_by(username=username).first()
        if user_to_login:
            return redirect(url_for('room1'))
        else:
            flash('Wrong credentials!', 'warning')
            return redirect(url_for('login'))
    return render_template('loginPage.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        confirm_password = request.form.get('confirmPassword')
        if bcrypt.check_password_hash(password, confirm_password):
            user = Users(username=username, password=password)
            try:
                db.session.add(user)
                db.session.commit()
                flash('You successfully created a new account!', 'info')
                return redirect(url_for('register'))
            except:
                flash('There was a problem creating this new account!', 'warning')
                return redirect(url_for('register'))
        else:
            flash('Please make sure that the password matches!', 'warning')
            return redirect(url_for('register'))
    return render_template('registerPage.html')


if __name__ == "__main__":
    app.run(debug=True)
