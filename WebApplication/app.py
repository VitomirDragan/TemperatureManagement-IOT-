from flask import Flask, render_template, request
from firebase import firebase

firebase = firebase.FirebaseApplication('https://temperaturemanagement-iot.firebaseio.com')

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def room1():
    temp1 = firebase.get('CurrentTempRoom1', 'Value')
    temp2 = firebase.get('CurrentTempRoom2', 'Value')
    hum1 = firebase.get('HumidityRoom1', 'Value')
    hum2 = firebase.get('HumidityRoom2', 'Value')
    if request.method == 'POST':
        variable = request.form['content']
        firebase.put('DesiredTempRoom1', 'Value', int(variable))
        return render_template('index.html', tempR1=temp1, tempR2=temp2, humR1=hum1, humR2=hum2)
    else:
        return render_template('index.html', tempR1=temp1, tempR2=temp2, humR1=hum1, humR2=hum2)

@app.route('/room2', methods=['POST','GET'])
def room2():
    temp1 = firebase.get('CurrentTempRoom1', 'Value')
    temp2 = firebase.get('CurrentTempRoom2', 'Value')
    hum1 = firebase.get('HumidityRoom1', 'Value')
    hum2 = firebase.get('HumidityRoom2', 'Value')
    if request.method == 'POST':
        variable = request.form['content2']
        firebase.put('DesiredTempRoom2', 'Value', int(variable))
        return render_template('index.html', tempR1=temp1, tempR2=temp2, humR1=hum1, humR2=hum2)
    else:
        return render_template('index.html', tempR1=temp1, tempR2=temp2, humR1=hum1, humR2=hum2)

if __name__ == "__main__":
    app.run(debug=True)





# firebase.put('DesiredTempRoom1', 'Value', 1)
#
# firebase.put('DesiredTempRoom2', 'Value', 30)
#
# while True:
#     result = firebase.get('CurrentTempRoom1', 'Value')
#     print("Temperature Room1:",result)
#     result = firebase.get('CurrentTempRoom2', 'Value')
#     print("Temperature Room2:", result)
#     sleep(5)
