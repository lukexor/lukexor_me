$(document).ready(function () {
  // Set active tab
  var currentPage = window.location.pathname;

  // Sets the navigation tab as active by hilighting it
  $('.nav-tabs a[href="' + currentPage + '"]').parent('li').addClass('active');

  // Disables any links on the page that match the current URL
  if ( window.location.search == '' ) {
    $('a[href="' + currentPage + '"]').addClass('disabled');
  }

  // Prevent disabled links from functioning
  $('body').on('click', 'a.disabled', function(event) {
    event.preventDefault();
  });

  // Form validation
  // Submit buttons are disabled by default until all required forms have
  // values
  $('#send-message').addClass('disabled'); // Set default to disabled
  $('#post-comment').addClass('disabled'); // Set default to disabled

  $('input').on('keyup blur change', function() { validateForm() });
  $('textarea').on('keyup blur change', function() { validateForm() });
}); // end document.ready

function validateForm() {
  var inputs = $('input.required'),
      textareas = $('textarea.required'),
      button = $('button[type="submit"]');

  fields = $.merge(inputs, textareas);

  var requiredCount = fields.size(),
      validCount = 0;

  // Ensure all required fields have values
  $.each(fields, function(index, field) {
    if ( $(field).val() ) { validCount += 1; }
  });

  if ( validCount === requiredCount ) {
    button.removeClass('disabled');
    return true;
  } else {
    button.addClass('disabled');
    return false;
  }
}
