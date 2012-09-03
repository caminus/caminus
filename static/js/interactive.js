$(document).ready(function() {
  $('#server-interaction .drawer').each(function() {
    var canvas = $(this).children('.canvas');
    $(this, '.drawer-label').click(function() {
      canvas.slideToggle("blind");
    });
  });
});
