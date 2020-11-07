function refresh(divId) { //Refreshing the div
    $(divId).load(" " + divId + " > *");
}

function callRefreshFunction() { //Call the function for div refreshing and giving as parameter the div`s id
    refresh("#monitorFirstRoom")
    refresh("#monitorSecondRoom")
}

$(document).ready( //Call periodically the function callRefreshFunction. The interval is set to 3 seconds
    setInterval(
        callRefreshFunction,
        3000,
    )
)