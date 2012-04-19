function updateBalance() {
    $.get("/api/balance", function(data) {
        $("#balance-display").html(data['balance']);
    });
}

function pollBalance() {
    updateBalance();
    window.setTimeout(pollBalance, 3000);
}

$(document).ready(function () {
    pollBalance();
});
