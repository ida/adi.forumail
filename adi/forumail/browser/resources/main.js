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
function setBrowserUrlWithoutReload(url) {
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
function changeUrlQuery(variable, values){
    var new_search = '?'
    // Get current search and remove questionmark of beginning:
    var search_string = window.location.search.substring(1)
    // Remove former var and its val(s) of current search:
    if(search_string.indexOf(variable) != -1) {
        // We have multiple paras:
        if(search_string.indexOf('&') != -1) {
            var searches = search_string.split('&')
            for(var i=0;i<searches.length;i++) {
                if(searches[i].split('=')[0] != variable) {
                    if(new_search != '?') {
                        new_search += '&'
                    }
                    new_search += searches[i]
                }
            }
        }
        // Just one para:
        else {
            if(search_string.split('=')[0] != variable) {
                new_search += search_string
            }
        }
    }
    // The passed var isn't present, keep complete old search:
    else {
        new_search += search_string
    }
    // Now, add new paras, we can have a list of vals, here:
    if(Array.isArray(values)) {
        for(var j=0;j<values.length;j++) {
            if(new_search != '?') {
                new_search += '&'
            }
            new_search += variable + '=' + values[j]
        }
    }
    // Or just one val:
    else {
        if(new_search != '?') {
            new_search += '&'
        }
        new_search += variable + '=' + values
    }
    // Get current url without search-query:
    var url = String(window.location).split('?')[0]
    // Set new query:
    setBrowserUrlWithoutReload(url + new_search)
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
function getAndSetSelection(threaded_class) {
    var threaded_links = $('.' + threaded_class + ' a')
    var selection = window.location.search.split('threaded=')[1]
    threaded_links.removeClass('selected')
    if(selection === undefined) {
        var selection = $(threaded_links[0]).attr('class')
    }
    $('.' + threaded_class + ' a.' + selection).addClass('selected')
}
function loadResults(eve, results_id) {
    eve.preventDefault()
    var url = $(eve.target).attr('href')
    setBrowserUrlWithoutReload(url)
    $('#' + results_id).load(link_url + ' #' + results_id + '-loader', function () {
        applyReplyListener()
    }); 
}
function applyReplyListener() {
    $('.reply.link').click(function(eve) {
        replyClicked(eve)
    });
}
function applyEventListeners(results_id, threaded_class) {
    $('.' + threaded_class + ' a').click(function(eve) {
        loadResults(eve, results_id)
        getAndSetSelection(threaded_class)
    });
    applyReplyListener()
}
function main() { if($('.section-forumail').length != -1) {

    var results_id = 'forum-body'
    var threaded_class = 'threaded'

    getAndSetSelection(threaded_class)

    applyEventListeners(results_id, threaded_class)
//////////////////////////////////////////////////////////////////////////////////////
$('.categories input').click(function() {
    var selected_categories = []
    $(this).parent().parent().find('input:checked ~ label').each(function() {
        selected_categories.push($(this).text())
    });
    console.debug(selected_categories)
});
//////////////////////////////////////////////////////////////////////////////////////
} /* EO .section-forumail */ } /* EO main */ main() }); /* EO doc.ready */ })(jQuery);

