(function($) { $(document).ready(function() {
function hideEditEles(parent_ele) {
    var hide_eles = [
'#portal-top',
'#portal-breadcrumbs',
'#content > div:nth-child(1)',
'#content > div:nth-child(2)',
'#archetypes-fieldname-description',
'#archetypes-fieldname-location',
'#archetypes-fieldname-language',
'#archetypes-fieldname-relatedItems',
'#archetypes-fieldname-image-caption',
'#archetypes-fieldname-image',
'#archetypes-fieldname-imageCaption',
'#archetypes-fieldname-title .formQuestion',
'#archetypes-fieldname-text .formQuestion',
'#archetypes-fieldname-subject .formQuestion',
'#cmfeditions_version_comment_block',
'.fieldTextFormat',
'#fieldset-dates',
'#fieldset-creators',
'#fieldset-settings',]
    parent_ele.find(hide_eles).hide()
}
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
    if (window.tinymce==undefined || !tinymce.editors.length) {
        setTimeout(checkTinyMCELoaded, 100)
        return
    }
    // Now we checked TinyMCE is loaded, set focus on its body-text-field:
    var richtext_body = $('#text_ifr').contents().find(".mceContentBody").get(0)
//tinyMCE.getInstanceById('text').focus();
}
function replyEditmode() {
    var title = document.referrer.split('&Title=')[1]
    $('#title').val(title).hide()
    setTimeout(checkTinyMCELoaded, 100);
}
function rrreplyClicked(eve) {
    eve.preventDefault()
    var hide_eles = getHideEles()
    var reply_form = $('<div id="reply-form" style="height: 0;">Reply form\</div>').insertAfter($(this).parent())
    reply_form.load(window.location.href + '/createObject?type_name=News+Item', function() {
        hideEditEles()
    });
}
function main() {
$('body').prepend(document.referrer)
if($('.template-forumail_view').length > 0) {
    $('.reply-to.link').click(function(eve) {
        history.pushState({}, '', $(this).attr("href"));
    });
}
if($('.template-atct_edit').length > 0) {
}
/* DEV:
*/
} /* EO main */ main() }); /* EO doc.ready */ })(jQuery);

