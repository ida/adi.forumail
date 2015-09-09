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
function loadResults(eve, results_id) {
    eve.preventDefault()
    var url = $(eve.target).attr('href')
console.debug(url)
    setUrlWithoutReload(url)
    $('#' + results_id).load(url + ' #' + results_id + '-loader', function () {
    }); 
}
function main() { if($('.section-forumail').length != -1) {
    var results_id = 'forum-body'
    $('.reply.link').click(function(eve) {
        replyClicked(eve)
    });
//////////////////////////////////////////////////////////////////////////////////////
    $('.sorting a').click(function(eve) {
console.debug('klk')
        loadResults(eve, results_id)
    });
//////////////////////////////////////////////////////////////////////////////////////
} /* EO .section-forumail */ } /* EO main */ main() }); /* EO doc.ready */ })(jQuery);

