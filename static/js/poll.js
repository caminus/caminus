function pollMessages() {
    $.get('/api/poll/0', function(data) {
      $('#balance-display').html(data['user-info']['balance']);
    });
}

function poll() {
    pollMessages();
    window.setTimeout(pollMessages, 3000);
}

$(document).ready(function () {
    poll();
});
