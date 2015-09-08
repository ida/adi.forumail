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
'#fieldset-settings',
    ]
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
// Thanks to Luca Fabbri, a.k.a. 'keul, for kindly sharing this snippet on:
// http://stackoverflow.com/questions/32088348
    if (window.tinymce==undefined || !tinymce.editors.length) {
        setTimeout(checkTinyMCELoaded, 100)
        return
    }
    doAfterTinyMCELoaded()
}
function replyClicked(eve) {
    eve.preventDefault()
    var link = $(eve.target)
    var title = link.attr("href").split('&Title=')[1]
    var reply_form = $('<div class="reply-form">Reply form\</div>').insertAfter(link.parent()).css({'height':'0','overflow':'hidden'})
    reply_form.load(window.location.href.split('?')[0] + '/createObject?type_name=News+Item', function() {
        hideReplyFormEles(reply_form)
        reply_form.find('#title').val(title).hide()
        reply_form.css('height', 'auto')
    });
    // Trigger waiting for TinyMCEditor to be loaded, 
    // which will execute doAfterTinyMCELoaded(), afterwards:
    setTimeout(checkTinyMCELoaded(), 100)
}
function getAndSetSelection(results_types_class) {
    var results_types_links = $('.' + results_types_class + ' a')
    var selection = window.location.search.split('results_type=')[1]
    results_types_links.removeClass('selected')
    if(selection === undefined) {
        var selection = $(results_types_links[0]).attr('class')
    }
    $('.' + results_types_class + ' a.' + selection).addClass('selected')
}
function loadResults(eve, results_id) {
    eve.preventDefault()
    var link_url = $(eve.target).attr('href')
    window.history.pushState(null, null, link_url)
    $('#' + results_id).load(link_url + ' #' + results_id + '-loader', function () {
        applyReplyListener()
    }); 
}
function applyReplyListener() {
    $('.reply.link').click(function(eve) {
        replyClicked(eve)
    });
}
function applyEventListeners(results_id, results_types_class) {
    $('.' + results_types_class + ' a').click(function(eve) {
        loadResults(eve, results_id)
        getAndSetSelection(results_types_class)
    });
    applyReplyListener()
}
function main() { if($('.section-forumail').length != -1) {

    var results_id = 'forum-body'
    var results_types_class = 'resultsTypes'
    var categories_class = 'categories'

    getAndSetSelection(results_types_class)

    applyEventListeners(results_id, results_types_class)
//////////////////////////////////////////////////////////////////////////////////////
$('.categories input').click(function() {
    var selected_categories = []
    $(this).parent().parent().find('input:checked ~ label').each(function() {
        selected_categories.push($(this).text())
    });
    console.log(selected_categories)
});
//////////////////////////////////////////////////////////////////////////////////////
} /* EO .section-forumail */ } /* EO main */ main() }); /* EO doc.ready */ })(jQuery);

