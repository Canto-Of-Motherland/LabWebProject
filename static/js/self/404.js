$(document).ready(function () {
    $(window).on('resize', function () {
      var windowHeight = $(window).height();
      if (windowHeight < 503) {
        $('.contact').hide();
        $('.split_link').hide();
        $('.link').hide();
      } else {
        $('.contact').show();
        $('.split_link').show();
        $('.link').show();
      }
    }).trigger('resize');
  });