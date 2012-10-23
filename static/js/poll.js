function pollMessages(id) {
    $.get('/api/poll/'+id, function(data) {
      if (id == 0)
        $('#chat-display').html('');
      $('#balance-display').html(data['user-info']['balance']);
      $(data['events']).each(function(idx, evt) {
        if (evt['type'] == "chat") {
          $('#chat-display').append("<li>"+evt['payload']['sender']+": "+evt['payload']['message']);
        } else if (evt['type'] == 'join') {
          $('#chat-display').append("<li><em>"+evt['payload']['player']+" has joined</em></li>");
        } else if (evt['type'] == 'quit') {
          $('#chat-display').append("<li><em>"+evt['payload']['player']+" has quit</em></li>");
        } else if (evt['type'] == 'broadcast') {
          $('#chat-display').append("<li><strong>"+evt['payload']['message']+"</strong></li>");
        }
      });
      window.setTimeout(function() {pollMessages(data['poll-id'])}, 1);
    });
}

function poll() {
    pollMessages(0);
}

$(document).ready(function () {
    poll();
});
