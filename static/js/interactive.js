$(document).ready(function() {
  $('#server-interaction .drawer').each(function() {
    console.log(this);
    var canvas = $(this).children('.canvas');
    $(this, '.drawer-label').click(function() {
      canvas.slideToggle("blind");
    });
  });
});
