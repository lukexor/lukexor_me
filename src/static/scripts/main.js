$(document).ready(function ()
{
    // Set active tab
    var current_page = window.location.pathname;
    $('.nav-tabs a[href="' + current_page + '"]').parent('li').addClass('active');

    if ( window.location.search == '' )
    {
        $('a[href="' + current_page + '"]').addClass('disabled');
    }


    // form validation
    $('#send-message').addClass('disabled'); // Set default to disabled
    $('#post-comment').addClass('disabled'); // Set default to disabled

    $('input').on('keyup blur change', function() { validate_form() });
    $('textarea').on('keyup blur change', function() { validate_form() });

    // Prevent disabled links from functioning
    $('body').on('click', 'a.disabled', function(event) {
        event.preventDefault();
    });
}); // end document.ready

function validate_form()
{
    var inputs = $('input.required'),
        textareas = $('textarea.required'),
        button = $('button[type="submit"]');

    fields = $.merge(inputs, textareas);

    var required_count = fields.size(),
        valid_count = 0;

    $.each(fields, function(c, field) {
        if ( $(field).val() ) { valid_count += 1; }
    });

    console.log("Valid: " + valid_count + ". Required: " + required_count);

    if ( valid_count === required_count )
    {
        button.removeClass('disabled');
        return true;
    }
    else
    {
        button.addClass('disabled');
        return false;
    }
}
