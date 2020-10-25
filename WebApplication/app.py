from flask import Flask, render_template, request, url_for
from firebase import firebase
from flask_sqlalchemy import SQLAlchemy

firebase = firebase.FirebaseApplication('https://temperaturemanagement-iot.firebaseio.com')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    admin_role = db.Column(db.Boolean, default=False)


@app.route('/', methods=['POST', 'GET'])
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


@app.route('/login')
def login():
    return render_template('registerPage.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('registerPage.html')


        # if request.method == 'POST':
        #     username = request.form['username']
        #     password = request.form['password']
        #     confirm_password = request.form['confirmPassword']
        #     if password == confirm_password:
        #         user = Users(username = username, password = password)
        #         db.session.add(user)
        #         db.commit()
        #         return render_template('controlPage.html', message = "You successfully created a new account!")
        #     else:
        #         return render_template('controlPage.html', message = "There was a problem creating this new account!")
        # return render_template('registerPage.html')


if __name__ == "__main__":
    app.run(debug=True)


