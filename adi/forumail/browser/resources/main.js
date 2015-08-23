(function($) { $(document).ready(function() {
function isNr(chara) {
    var IS_NR = '0'; var nrs = ['1','2','3','4','5','6','7','8','9','0']
    for(var i=0;i<nrs.length;i++) { if(chara == nrs[i]) { IS_NR = '1' } }
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
function setTitleOfUrlPara() {
    // Get everything after 'Title='
    var title = document.referrer.split('Title=')[1]
    // If there's more paras following, get everything until next para:
    if(document.referrer.indexOf('&') != -1) { title = title.split('&')[0] }
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
    setTitleOfUrlPara()
    setTimeout(checkTinyMCELoaded, 100); // sets focus on body-text-field
}
function setBrowserUrlWithoutReload(url) {
    window.history.pushState(null, '', url)
}
function removeAllUrlParas() {
    var browser_url = window.location.href
    if(browser_url.indexOf('?') != -1) { browser_url = browser_url.split('?')[0] }
    return browser_url
}
function clickReply(link, eve) {
    var link_url = $(link).attr('href')
    setBrowserUrlWithoutReload(link_url)
}
function main() {

    if($('.template-forumail_view').length > 0) {
        $('.reply').click(function(eve) {
            clickReply($(this), eve)
        });
    }

    if($('.template-atct_edit.section-forumail').length > 0) {
        var title = document.referrer.split('&Title=')[1]
        $('#title').val(title).hide()
        setTimeout(checkTinyMCELoaded, 100); // sets focus on body-text-field
    }


} /* EO main */ main() }); /* EO doc.ready */ })(jQuery);

