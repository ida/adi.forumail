# -*- coding: utf-8 -*-

from plone import api

from Acquisition import aq_inner, aq_parent

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class View(BrowserView):

    index = ViewPageTemplateFile("forum_main.pt")

    forum_head = ViewPageTemplateFile("forum_head.pt")

    posts_template = ViewPageTemplateFile("forum_body.pt")

    def getResultsTypes(self):
        return ['posts', 'threads']

    def getPostPortalType(self):
        return 'News Item'

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def renderForumHead(self):
        return self.forum_head()

    def renderForumBody(self):
        return self.posts_template()

    def getForumUrl(self):
        forum_url = self.request["ACTUAL_URL"]
        context = aq_inner(self.context)
        if context.Type() == self.getPostPortalType():
            forum_url = '/'.join(forum_url.split('/')[:-1])
        return forum_url

    def getForumPath(self):
        context = aq_inner(self.context)
        forum_path = self.request["ACTUAL_URL"]
        if context.Type() == self.getPostPortalType():
            forum_path = '/'.join(forum_path.split('/')[:-1])
        return forum_path

    def getAddUrl(self):
        add_url = None
        forum_url = self.getForumUrl()
        if forum_url:
            add_url = forum_url + '/createObject?type_name=' + self.getPostPortalType()
        return add_url

    def getUrlParas(self):
        pairs = self.request.form.keys()
        return pairs

    def getUrlParaVal(self, para):
        val = self.request.form[para]
        return val

    def getResultsType(self):
        para = 'results_type'
        results_type = self.getResultsTypes()[0] # default
        paras = self.getUrlParas()
        if para in paras:
            results_type = self.getUrlParaVal(para)
        return results_type

    def getPostsResult(self):
        """ Main function to return list of posts to view."""
        results = None
        results_type = self.getResultsType()
        if results_type == 'posts':
            results = self.getPosts()
        elif results_type == 'threads':
            results = self.getThreads()
        else:
            raise Exception, 'Results-type "' + results_type + '" is not available'
        return results

    def getPosts(self, sort_order='reverse', sort_on='created'):
        """
        Expects forum-container-folder or one of its first-children, : A post.
        Returns all posts of forum, as a catalog-brain-dict, not as objects.
        """
        context = aq_inner(self.context)
        if context.Type() == self.getPostPortalType():
            context = aq_parent(context)
        elif context.Type() != 'Folder':
            raise Exception, context.Type() + " is not considered to be a forum's child, yet."
        posts = api.content.find(context=context,
                                 portal_type=self.getPostPortalType(),
                                 sort_on=sort_on,
                                 sort_order=sort_order)
        return posts

    def getPostsIds(self):
        post_ids = []
        posts = self.getPosts()
        for post in posts:
            post_id = post['id']
            post_ids.append(post_id)
        return post_ids

    def getThreadId(self, post_id):
        thread_id = None
        nrs = ['0','1','2','3','4','5','6','7','8','9']
        i = len(post_id)-1
        if post_id[-1] in nrs:
            while i > 0 and post_id[i] in nrs or post_id[i] == '-':
                i -= 1
                if post_id[i] == '-' and not post_id[i-1] in nrs:
                    break
            thread_id = post_id[:i]
        else:
            thread_id = post_id
        return thread_id

    def getThreadsIds(self):
        threads_ids = []
        posts_ids = self.getPostsIds()
        for post_id in posts_ids:
            thread_id = self.getThreadId(post_id)
            if thread_id not in threads_ids:
                threads_ids.append(thread_id)
        return threads_ids

    def getThreads(self):
        """
        Sorted by containing newest post.
        """
        threads_flat = []   # endresult
        threads_nested = [] # [ [threadposts], ]
        thread = None
        thread_ids = []
        threads_ids = self.getThreadsIds()
        posts = self.getPosts()

        for thread_id in threads_ids:
            
            i = -1
            while i < len(posts)-1:
                i += 1
            
                post = posts[i]
                post_id = post['id']
                

                if post_id == thread_id: # found threadstarter
                    thread = [posts[i]]

            
                    i = -1 # start searching from begin of list for replies
                    while i < len(posts)-1:
                        i += 1
            
                        post = posts[i]
                        post_id = post['id']
                        # TODO: make this sharper (endswith numbers sep by minus...):
                        if post_id.startswith(thread_id) and post_id != thread_id:
                            thread.append(posts[i]) # found reply
#                    print ', '.join([str(post['id']) for post in thread])
                    threads_nested.append(thread)
        # Sort a thread alphabetically by id: 
        for thread in threads_nested:
            thread_new = self.sortById(thread)
            for post in thread_new:
                threads_flat.append(post)
        return threads_flat

    def isReply(self, post_id, thread_id):
        IS_REPLY = False
        nrs = ['1','2','3','4','5','6','7','8','9','0']
        if len(post_id) >= len(thread_id) + 1 \
        and post_id.startswith(thread_id + '-')\
        and post_id[len(thread_id) + 1] in nrs:
            IS_REPLY =  True
        return IS_REPLY

    def isIniPost(self, post_id):
        IS_INI_POST = False
        thread_id = self.getThreadId(post_id)
        IS_REPLY = self.isReply(post_id, thread_id)
        if not IS_REPLY: IS_INI_POST = True
        return IS_INI_POST

    def sortById(self, posts):
        new_posts = []
        posts_ids = []
        for post in posts:
            posts_ids.append(post['id'])
        posts_ids.sort()
        for post_id in posts_ids:
            for post in posts:
                if post['id'] == post_id:
                    new_posts.append(post)
        return new_posts

    def getPostsMarkup(self):
        """DEV: Experimental."""
        posts = ()
        post = ()
        reply_id = None
        field_names = ['id', 'Title', 'Subject', 'created', 'Creator']
        result = self.getPostsResult()
        for item in result:
            post = '<div class="post">'
            post += '<div class="head">'
            for field_name in field_names:
                value = item[field_name]
                if field_name == 'id':
                    thread_id = self.getThreadId(value)
                    reply_id = value[len(thread_id):]
                    #if reply_id == '': reply_id  = '-'
                    reply_id = '0' + reply_id
                    post += '<span class="' + field_name.lower() + '">' + reply_id + '</span>'
                elif field_name == 'Title':
                    if reply_id == '0':
                        post += '<a class="' + field_name.lower() + '" href="' + value + '">' + value + '</a>'
                elif field_name == 'created':
                    creation_date = str(value)[:16]
                    post += '<span class="' + field_name.lower() + '">' + creation_date + '</span>'

                else:
                    post += '<span class="' + field_name.lower() + '">'
                    if type(value) is tuple: #keywords, a.k.a. tags/categories of field_name 'Subject'
                        for val in value:
                            post += '<span class="' +  str(val) + '">'
                            post += val
                            post += '</span>'
                    else:
                        post += str(value)
                    post += '</span>'

            post += '</div>' # .post .head
            post += '<div class="body">'
            post += item.getObject().getText()
            post += '</div>' # .post .body
            post += '</div>' # .post
            posts += (post,)
        return posts


#EOF
