(function($) { $(document).ready(function() {
function setRepliesIndent(posts) {
    $(posts).each(function() {
        var post = $(this)
        var post_title = post.find('.summary')
        var text = post_title.text()
        var indent = 0
        while( text.startsWith('Re: ') ) {
            indent += 1
            text = text.substring(4, text.length)
        }
        post.css('margin-left', String(indent) + 'em')
    });
}
function wrapMailQuotations(posts) {
    // Wrap quotations into a div and hide it.
    $(posts).each(function() {
        var post = $(this)
        var post_body = post.find('div p')
        var post_message = post_body.html()
        var lines = post_message.split('<br>')
        var digest = ''

        // Collect quots start and end posis:
        var i = -1
        while(i<lines.length-1) {
            i += 1
            var line = lines[i]
            if(line.startsWith('&gt;')){
                digest += '<span class="toggle">Hide</span><div class="quotation">'
                while(line.startsWith('&gt;') && i<lines.length-1){
                    i += 1
                    line = lines[i]
                    digest += line + '<br>'
                }
                digest += '</div>'
            }
            digest += line + '<br>'
        }
    post_body.html(digest)
    }); // each post
}
function toggleQuotVisi(button) {
    var post = button.parent()
    post.find('div div').toggle()
    if(button.text() == 'Hide'){
        button.text('Show')    
    }
    else {
        button.text('Hide')    
    }
}
function main() {
    var posts = $('#content-core .item')
    setRepliesIndent(posts)
    wrapMailQuotations(posts)
    $('#content-core .toggle').click(function(){
        $(this).find('~ *').toggle()
        if($(this).text()=='Hide'){
            $(this).text('Show')        
        }
        else {
            $(this).text('Hide')
        }
    });
    $('#content-core .toggle').click() // ini hide
}
main() }); })(jQuery);
