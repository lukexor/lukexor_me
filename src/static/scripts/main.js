$(document).ready(function ()
{
    // Set active tab
    var current_page = window.location.pathname;
    $('.nav-tabs a[href="' + current_page + '"]').parent('li').addClass('active');

    if (window.location.search == '')
    {
        $('a[href="' + current_page + '"]').addClass('disabled');
    }


    // form validation
    $('#send_message').addClass('disabled'); // Set default to disabled
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
    var $input  = $('input.required'),
        $text   = $('textarea.required'),
        $button = $('button[role="submit"]');

    var forms_valid = true;

    $input.each(function()
    {
        if (!$(this).val())
        {
            console.log($(this).attr('value') + "is not valid.");
            forms_valid = false;
        }
    });

    if (forms_valid && $text.val())
    {
        $button.removeClass('disabled');
    }
    else
    {
        $button.addClass('disabled');
    }
}
