function sendChat(message) {
  $.post('/api/chat', {'message': message}, function(data) {
    $('#chat-line').val('');
    $('#chat-line').disabled = false;
  });
}

$(document).ready(function() {
  $('#server-interaction .drawer').each(function() {
    var canvas = $(this).children('.canvas');
    $(this).children('.drawer-label').click(function() {
      canvas.slideToggle("blind");
    });
  });
  $('#chat-line').keypress(function(evt) {
    if (evt.charCode == 13) {
      $('#chat-line').disabled = true;
      sendChat($('#chat-line').val());
    }
  });
});
