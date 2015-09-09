(function($) { $(document).ready(function() {
function hideReplyFormEles(parent_ele) {
    var hide_eles = [
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
/*
'#archetypes-fieldname-language',
'#archetypes-fieldname-relatedItems',
'#archetypes-fieldname-subject .formQuestion',
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
    setTimeout(checkTinyMCELoaded(), 100)
}
function loadResults(eve, results_id) {

    eve.preventDefault()

    var url = $(eve.target).attr('href')

    setUrlWithoutReload(url)

    $('#' + results_id).load(url + ' #' + results_id + '-loader', function (response, status, xhr) {
        if(status == "error") {
            var msg1 = '<div>Sorry, but there was an error:</div>'
            var msg2 = '<div>Please reload the page, you should get the selected results, then.</div>'
            $('<div class="error">' + msg + xhr.status + ' ' + xhr.statusText + msg2 + '</div>').insertAfter('#' + results_id)
        }
        reApplyEventListeners()
    });
}
function reApplyEventListeners() {
    $('.reply.link').click(function(eve) {
        replyClicked(eve)
    });
}
function iniApplyEventListeners(results_id) {
    $('.reply.link').click(function(eve) {
        replyClicked(eve)
    });
    $('.sorting a').click(function(eve) {
        loadResults(eve, results_id)
    });
}
function endswith(str, sub) {
    if( str.sub(0, sub.length == sub) ) { return true }
    else { return false }
}
function main() { if($('.section-forumail').length != -1) {
    
    var results_id = 'forum-body'
    
    iniApplyEventListeners(results_id)

//   if($('.template-atct_edit').length != -1) {
    $('')click
        $('script').each(function () {
            if( endswith(String($(this).attr('src')), '/form_tabbing.js') ) {
console.log('AHOI!')
                $(this).remove()
            }
        });
//    }

} /* EO .section-forumail */ } /* EO main */ main() }); /* EO doc.ready */ })(jQuery);

