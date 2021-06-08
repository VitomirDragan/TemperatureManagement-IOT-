// Firebase configuration object, needed to initialize the application
const firebaseConfig = {
    apiKey: "AIzaSyChtewPO_zJyGpABQp9IhedRdgLMglVKfg",
    authDomain: "temperaturemanagement-iot.firebaseapp.com",
    databaseURL: "https://temperaturemanagement-iot.firebaseio.com",
    projectId: "temperaturemanagement-iot",
    storageBucket: "temperaturemanagement-iot.appspot.com",
    messagingSenderId: "390182663875",
    appId: "1:390182663875:web:0367ba031cee568e109476",
    measurementId: "G-ZF61CXHKLK"
};
firebase.initializeApp(firebaseConfig); // Web application is configured to use firebase

// Login to database
function Login(username, password) {
    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION); // The connection will be interrupted when web tab is clossed
    firebase.auth().signInWithEmailAndPassword(username, password).catch(e => alert(e.message)); // Sign in with email and password
}


if (window.location.pathname === '/home') { // Execute the following instructions if the route is '/home'

    // Read CurrentTempRoom1 field only when the value is updated in database
    firebase.database().ref('CurrentTempRoom1/').on('value', function (snapshot) {
        document.getElementById('temperatureRoom1').value = snapshot.val().Value;
    });

    // Read CurrentTempRoom2 field only when the value is updated in database
    firebase.database().ref('CurrentTempRoom2/').on('value', function (snapshot) {
        document.getElementById('temperatureRoom2').value = snapshot.val().Value;
    });

    // Read HumidityRoom1 field only when the value is updated in database
    firebase.database().ref('HumidityRoom1/').on('value', function (snapshot) {
        document.getElementById('humidityRoom1').value = snapshot.val().Value;
    });

    // Read HumidityRoom2 field only when the value is updated in database
    firebase.database().ref('HumidityRoom2/').on('value', function (snapshot) {
        document.getElementById('humidityRoom2').value = snapshot.val().Value;
    });

    // Read DesiredTempRoom1/Zapier field only when the value is updated in database
    firebase.database().ref('DesiredTempRoom1/Zapier').on('value', function (snapshot) {
        document.getElementById('outputValue1').value = snapshot.val().Value;
        document.getElementById('rangeValueRoom1').value = snapshot.val().Value;
    });

    // Read DesiredTempRoom2/Zapier field only when the value is updated in database
    firebase.database().ref('DesiredTempRoom2/Zapier').on('value', function (snapshot) {
        document.getElementById('outputValue2').value = snapshot.val().Value;
        document.getElementById('rangeValueRoom2').value = snapshot.val().Value;
    });
}
