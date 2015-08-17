(function($) { $(document).ready(function() {
function main() {

    // If in collection-view, prepend dot to reply-to-links,
    // so reply will be created in container not in collection:
    if($('.section-forumail.portaltype-topic').length > 0) {
        $('.item #portlets-below a').each(function() {
            $(this).attr('href', '.' + $(this).attr('href'))
        }); // each reply-to-link
    }

    // If in edit-mode and url contains a hash ...
    if($('.section-forumail.template-atct_edit').length > 0 && window.location.href.indexOf('#') != -1) {
        // ... we are in a reply and set the title to be anything following after url-hash:
        var title = window.location.href.split('#')[1]
        $('#title').val(title)
        $('#text').val('<a href="#">a</a>')
        $('#text_text_format').focus()
        $('#title').parent().hide()
    }
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
} /* EO main */ main() }); /* EO doc.ready */ })(jQuery);
