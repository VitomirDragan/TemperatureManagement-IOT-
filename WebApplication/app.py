from flask import Flask, render_template, request
from firebase import firebase
from time import sleep

firebase = firebase.FirebaseApplication('https://temperaturemanagement-iot.firebaseio.com')

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def room1():
    result = firebase.get('CurrentTempRoom1', 'Value')
    result2 = firebase.get('CurrentTempRoom2', 'Value')
    if request.method == 'POST':
        variable = request.form['content']
        firebase.put('DesiredTempRoom1', 'Value', int(variable))
        return render_template('index.html', data1=result, data2=result2)
    else:
        return render_template('index.html', data1=result, data2=result2)

@app.route('/room2', methods=['POST','GET'])
def room2():
    result = firebase.get('CurrentTempRoom1', 'Value')
    result2 = firebase.get('CurrentTempRoom2', 'Value')
    if request.method == 'POST':
        variable = request.form['content2']
        firebase.put('DesiredTempRoom2', 'Value', int(variable))
        return render_template('index.html', data1=result, data2=result2)
    else:
        return render_template('index.html', data1=result, data2=result2)

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
