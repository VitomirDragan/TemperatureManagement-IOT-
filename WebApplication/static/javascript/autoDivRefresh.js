$(document).ready(function () {
    setInterval(function () {
        $("#divToBeRefreshed").load(window.location.href + " #divToBeRefreshed");
    }, 3000);
});