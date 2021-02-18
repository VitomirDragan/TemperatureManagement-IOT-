var firebaseConfig = {
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
const auth = firebase.auth();

firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION);
const promise = auth.signInWithEmailAndPassword("webapplication@gmail.com", "webApplication");
console.log("logged in");
// promise.catch(e => alert(e.message));
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

// function Logout() {
//     auth.signOut();
//     console.log("logged out")
// }


// const addBtn = document.getElementById('submitButtonRoom2');
//
// addBtn.addEventListener('click',(e)=>{
//     e.preventDefault();
//     database.ref('DesiredTempRoom2/Zapier').set(
//         {
//             Value: temperatureSetR1
//         });
// });

// document.getElementById('submitButtonRoom1').onclick = function () {
//     const temperatureSetR1 = document.getElementById("desiredTemperatureRoom1").value;
//     firebase.database().ref('DesiredTempRoom1/Zapier').set(
//         {
//             Value: parseInt(temperatureSetR1)
//         }
//     )
// };

firebase.database().ref('DesiredTempRoom1/Zapier').on('value', function (snapshot) {
    document.getElementById('outputValue1').value = snapshot.val().Value;
    document.getElementById('rangeValueRoom1').value = snapshot.val().Value;
});

firebase.database().ref('DesiredTempRoom2/Zapier').on('value', function (snapshot) {
    document.getElementById('outputValue2').value = snapshot.val().Value;
    document.getElementById('rangeValueRoom2').value = snapshot.val().Value;
});
