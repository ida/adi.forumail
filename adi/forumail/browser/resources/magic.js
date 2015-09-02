(function($) { $(document).ready(function() {
function hideReplyFormEles(parent_ele) {
    var hide_eles = [
'#portal-top',
'#portal-breadcrumbs',
'#content > div:nth-child(1)',
'#content > div:nth-child(2)',
'#archetypes-fieldname-description',
'#archetypes-fieldname-location',
'#archetypes-fieldname-language',
'#archetypes-fieldname-relatedItems',
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
function doAfterTinyMCELoaded() {
    tinyMCE.getInstanceById('text').focus()
    $('ul.formTabs').hide()
    $('.reply.link').remove()
}
function checkTinyMCELoaded() {
// Thanks to Luca Fabbri, a.k.a. for kindly sharing this snippet:
// http://stackoverflow.com/questions/32088348
    if (window.tinymce==undefined || !tinymce.editors.length) {
        setTimeout(checkTinyMCELoaded, 100)
        return
    }
    doAfterTinyMCELoaded()
}
function replyClicked(link, eve) {
    eve.preventDefault()
    var title = link.attr("href").split('&Title=')[1]
    var reply_form = $('<div id="reply-form">Reply form\</div>').insertAfter(link.parent()).css({'height':'0','overflow':'hidden'})
    reply_form.load(window.location.href.split('?')[0] + '/createObject?type_name=News+Item', function() {
        hideReplyFormEles(reply_form)
        reply_form.find('#title').val(title).hide()
        reply_form.css('height', 'auto')
    });
    // Trigger waiting for TinyMCEeditor to be loaded, 
    // which will execute doAfterTinyMCELoaded(), afterwards:
    setTimeout(checkTinyMCELoaded(), 100)
}
function loadResults(eve) {
    eve.preventDefault()
    var link = $(eve.target)
    var link_url = link.attr('href')
    if(link.parent().hasClass('resultsType')) {
        window.history.pushState(null, null, link_url)
       $('#forumail-posts').load(link_url +' #forumail-posts') 
    }
}
function main() {
    $('.reply.link').click(function(eve) {
        replyClicked($(this), eve)
    });
    $('.forumail > .head .sorting').click(function(eve) {
        loadResults(eve)
    });
} /* EO main */ main() }); /* EO doc.ready */ })(jQuery);

