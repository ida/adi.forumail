(function($) { $(document).ready(function() {
function replyFormHideEles(parent_ele) {
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
    for(var i=0;i<hide_eles.length; i++) {
        parent_ele.find(hide_eles[i]).hide()
    }
}
function replyClicked(link, eve) {
    eve.preventDefault()
    var title = link.attr("href").split('&Title=')[1]
    var reply_form = $('<div id="reply-form">Reply form\</div>').insertAfter(link.parent()).css({'border':'1px solid red','height':'0','overflow':'hidden'})
    reply_form.load(window.location.href + '/createObject?type_name=News+Item', function() {
        replyFormHideEles(reply_form)
        reply_form.find('#title').val(title).hide()
        reply_form.css('height', 'auto')
    });
}
function main() {
    $('.reply.link').click(function(eve) {
        replyClicked($(this), eve)
    });
} /* EO main */ main() }); /* EO doc.ready */ })(jQuery);

