function updateServer() {
    $.get("/api/server/dev.camin.us", function(data) {
        hours = parseInt((data['time']/1000)+8)%24;
        minutes = parseInt(((data['time']/1000)%1)*60);
        var day = hours < 12;
        minutes = ""+minutes;
        while(minutes.length<2)
            minutes = "0"+minutes;
        $("#time-display").html(hours+":"+minutes+" "+(day ? "am":"pm"));
    });
}

function pollServer() {
    updateServer();
    window.setTimeout(pollServer, 1000);
}

$(document).ready(function () {
    pollServer();
});
