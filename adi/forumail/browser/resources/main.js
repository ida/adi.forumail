(function($) { $(document).ready(function() {
function hideReplyFormEles(parent_ele) {
    var hide_eles = [
'#portal-footer-wrapper',
'#portal-top',
'#portal-breadcrumbs',
'#content > div:nth-child(1)',
'#content > div:nth-child(2)',
'#archetypes-fieldname-title .formQuestion',
'#archetypes-fieldname-description',
'#archetypes-fieldname-text .formQuestion',
'.fieldTextFormat',
'#archetypes-fieldname-image',
'#archetypes-fieldname-imageCaption',
'#archetypes-fieldname-location',
'#cmfeditions_version_comment_block',
// Add-form:
'#archetypes-fieldname-language',
'#archetypes-fieldname-relatedItems',
'#archetypes-fieldname-subject .formQuestion',
/* Rest of fieldsets. Visible, if JS is disabled:
'#fieldset-dates',
'#fieldset-creators',
'#fieldset-settings',
*/
    ]
    for(var i=0;i<hide_eles.length; i++) {
        parent_ele.find(hide_eles[i]).hide()
    }
}
function setUrlWithoutReload(url) {
    window.history.pushState(null, '', url)
}
function getUrlQueryVarVals(variable) {
    var vals = []
    var query = window.location.search.substring(1)
    var vars = query.split("&")
    for (var i=0;i<vars.length;i++) {
            var pair = vars[i].split("=")
            if(pair[0] == variable) {
                vals.push(pair[1])
            }
    }
    return(vals)
}
function doAfterTinyMCELoaded(ini) {
    if(ini=='false') {
        tinyMCE.getInstanceById('text').focus()
    }
    else {
        $('#fieldset-categorization').show()
    }
    $('ul.formTabs').hide()
    $('.add').remove()
    $('.reply').remove()
}
function checkTinyMCELoaded(ini) {
    // Thanks to Luca Fabbri, a.k.a. 'keul', for kindly sharing this snippet on:
    // http://stackoverflow.com/questions/32088348
    if (window.tinymce==undefined || !tinymce.editors.length) {
        setTimeout(checkTinyMCELoaded, 100)
        return
    }
    doAfterTinyMCELoaded(ini)
}
function replyClicked(eve, ini='false') {

    eve.preventDefault()

    var link = $(eve.target)
    var title = link.attr("href").split('&Title=')[1]
    var reply_form = $('<div class="reply-form">Reply form\</div>')
                     .insertAfter(link.parent())
                     .css({'height':'0','overflow':'hidden'})

    reply_form.load(window.location.href.split('?')[0] + '/createObject?type_name=News+Item', function() {

        hideReplyFormEles(reply_form)

        if(ini=='false') {
            reply_form.find('#title').val(title).hide()
        }

        reply_form.css('height', 'auto')

    });

    setTimeout(checkTinyMCELoaded(ini), 100)

}
function addClicked(eve) {
    replyClicked(eve, ini=true)
}
function loadResults(eve, results_id) {

    eve.preventDefault()

    var url = $(eve.target).attr('href')

    setUrlWithoutReload(url)

    $('#' + results_id).load(url + ' #' + results_id + '-loader', function (response, status, xhr) {
        if(status == "error") {
            var msg1 = '<div>Sorry, but there was an error:</div>'
            var msg2 = '<div>Please reload the page, you should get the selected results, then.</div>'
            $('<div class="error">' + msg1 + xhr.status + ' ' + xhr.statusText + msg2 + '</div>').insertAfter('#' + results_id)
        }
        reApplyEventListeners()
    });
}
function reApplyEventListeners() {
    $('.add').click(function(eve) { addClicked(eve) });
    $('.reply').click(function(eve) { replyClicked(eve) });
}
function iniApplyEventListeners(results_id) {
    $('.sorting a').click(function(eve) { loadResults(eve, results_id) });
    reApplyEventListeners()
}
function endswith(str, sub) {
    if( str.substr(0, sub.length == sub) ) { return true }
    else { return false }
}
function main() { if($('.section-forumail').length != -1) {
    
    var results_id = 'forum-body'
    
    iniApplyEventListeners(results_id)

} /* EO .section-forumail */ } /* EO main */ main() }); /* EO doc.ready */ })(jQuery);

