(function($) { $(document).ready(function() {
function isNr(chara) {
    IS_NR = '0'
    var nrs = ['1','2','3','4','5','6','7','8','9','0']
    for(var i=0;i<nrs.length;i++) {
        if(chara == nrs[i]) {
            IS_NR = '1'
        }
    }
    return IS_NR
}
function indentReply(post_link) {
    var url = post_link.attr('href')
    var indent_depth = 0
    var i = url.length-1
    var chara = url[i]
    // Get indent-depth:
    while(i > -1 && isNr(chara) == '1' || chara == '-') {
        if(chara == '-') {
            indent_depth += 1
        }
        i -= 1
        chara = url[i]
    } // while is nr or minus
    // Set indent:
    if(indent_depth > 0) {
        post_link.parent().parent().css('margin-left', indent_depth + 'em')
    }
}
function adjustReplyToPath(reply_to_link) {
    // If in collection-view, prepend dot to reply-to-links,
    // so reply will be created in container, not in collection:
    reply_to_link.attr('href', '.' + reply_to_link.attr('href'))
}
function setTitleOfUrlHash() {
    // Get hashtag of url:
    var title = window.location.href.split('#')[1]
    // Set hashtag as title:
    $('#title').val(title)
    // Hide field, so user cannot damage auto-title:
    $('#title').parent().hide()
}
function checkTinyMCELoaded () {
    // This snippet was kindly shared by Luca Fabbri a.k.a. 'keul' on:
    // stackoverflow.com/questions/32088348/how-to-set-focus-on-rich-text-field-in-edit-mode-of-a-contenttype
    // Make sure to check out his blog, too: http://blog.keul.it/
    if (window.tinymce==undefined || !tinymce.editors.length) {
        setTimeout(checkTinyMCELoaded, 100)
        return
    }
    // Now we checked TinyMCE is loaded, set focus on its body-text-field:
    $('#text_ifr').contents().find(".mceContentBody").get(0).focus()
}
function manipulateReplyEditform() {
    setTitleOfUrlHash()
    setTimeout(checkTinyMCELoaded, 100); // sets focus on body-text-field
}
function main() {

    // Is listview:
    if($('.section-forumail.portaltype-topic').length > 0) {
        $('.item #portlets-below a').each(function() { adjustReplyToPath($(this)) });
        $('.headline a').each(function() { indentReply($(this)) });
    }

    // Is editview and a reply, because url contains a hash:
    if($('.section-forumail.template-atct_edit').length > 0 && window.location.href.indexOf('#') != -1) {
        manipulateReplyEditform()
    }

} /* EO main */ main() }); /* EO doc.ready */ })(jQuery);

