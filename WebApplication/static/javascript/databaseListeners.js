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
firebase.initializeApp(firebaseConfig);
function Login(username, password){
    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION);
    firebase.auth().signInWithEmailAndPassword(username, password).catch(e => alert(e.message));
}

if (window.location.pathname === '/home') {
    firebase.database().ref('CurrentTempRoom1/').on('value', function (snapshot) {
        document.getElementById('temperatureRoom1').value = snapshot.val().Value;
    });

    firebase.database().ref('CurrentTempRoom2/').on('value', function (snapshot) {
        document.getElementById('temperatureRoom2').value = snapshot.val().Value;
    });

    firebase.database().ref('HumidityRoom1/').on('value', function (snapshot) {
        document.getElementById('humidityRoom1').value = snapshot.val().Value;
    });

    firebase.database().ref('HumidityRoom2/').on('value', function (snapshot) {
        document.getElementById('humidityRoom2').value = snapshot.val().Value;
    });

    // document.getElementById('outputValue1').addEventListener('change', (e) => {
    //     // e.preventDefault();
    //     const temperatureSetR1 = document.getElementById("outputValue1").value;
    //     firebase.database().ref('DesiredTempRoom1/Zapier').set(
    //         {
    //             Value: parseInt(temperatureSetR1)
    //         });
    // });

    // document.getElementById('outputValue2').addEventListener('change', (e) => {
    //     e.preventDefault();
    //     const temperatureSetR2 = document.getElementById("outputValue2").value;
    //     firebase.database().ref('DesiredTempRoom2/Zapier').set(
    //         {
    //             Value: parseInt(temperatureSetR2)
    //         });
    // });

    firebase.database().ref('DesiredTempRoom1/Zapier').on('value', function (snapshot) {
        document.getElementById('outputValue1').value = snapshot.val().Value;
        document.getElementById('rangeValueRoom1').value = snapshot.val().Value;
    });

    firebase.database().ref('DesiredTempRoom2/Zapier').on('value', function (snapshot) {
        document.getElementById('outputValue2').value = snapshot.val().Value;
        document.getElementById('rangeValueRoom2').value = snapshot.val().Value;
    });
}
