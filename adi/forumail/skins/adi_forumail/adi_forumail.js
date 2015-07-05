(function($) { $(document).ready(function() {
$("#visual-portal-wrapper").prepend("Congrats, adi_forumail.js has been loaded succesfully!")


// Add indent to post, if starting with 'Re: ':
$('.summary').each(function() {
    var indent = 0
    var text = $(this).text()
    // Add one indent per 'Re: ':
    while( text.startsWith('Re: ') ) {
        indent += 1
        text = text.substring(4, text.length)
    }
    // Set indent:
    $(this).parent().parent().css('margin-left', String(indent) + 'em')
}); // each




}); })(jQuery);
