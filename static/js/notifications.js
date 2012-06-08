$(document).ready(function () {
  $("#notification-ack-form").submit(function(evt) {
    evt.preventDefault();
    $("#notifications-block").slideUp();
    $.get(uris['local.views.mark_notifications_read']);
  });
});
