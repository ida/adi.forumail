# -*- coding: utf-8 -*-

from adi.forumail import post_portal_type
from adi.forumail import bool_false_symbolic_strings
from adi.forumail import bool_true_symbolic_strings
from plone import api
from Acquisition import aq_inner, aq_parent
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class View(BrowserView):

    index = ViewPageTemplateFile("forum_main.pt")

    forum_head = ViewPageTemplateFile("forum_head.pt")

    forum_body = ViewPageTemplateFile("forum_body.pt")

    def __call__(self):
        return self.render()

    def exchangeParaVal(self, query, para, val):
        query_splits = query.split(para)
        query_start = query_splits[0]
        query_rest = query_splits[1]
        query_rest_splits = query_rest.split('&')
        query_end_splits = query_rest_splits[1:]
        if type(query_end_splits) == list:
            query_end = '&'.join(query_end_splits)
        else:
            query_end = query_end_splits
        if query_end != '': query_end = '&' + query_end
        query = query_start + para + '=' + val + query_end
        return query

    def getAddUrl(self):
        add_url = None
        forum_url = self.getForumUrl()
        if forum_url:
            add_url = forum_url + '/createObject?type_name=' + post_portal_type
        return add_url

    def getForumUrl(self):
        forum_url = None
        context = aq_inner(self.context)
        if context.Type() == post_portal_type:
            context = aq_parent(self.context)
        forum_url = context.absolute_url()
        return forum_url

    def getPosts(self):
        cats = []
        context = aq_inner(self.context)
        if context.Type() == post_portal_type:
            context = aq_parent(self.context)
        if self.getUrlParaVal('Subject'):
            cats self.getUrlParaVal('Subject')
        posts = api.content.find(context=context,
                                 portal_type=post_portal_type,
                                 Subject=cats,
                                 sort_on='created',
                                 sort_order='reverse')
        return posts

    def getReplyDepth(self, post_id):
        return self.getReplyIdAndDepth(post_id)[1]

    def getReplyDepthIter(self, post_id):
        reply_iters = ()
        i = self.getReplyDepth(post_id) + 1
        for j in range(i-1): # minus one to exclude orig-text-ele
            reply_iters += ('i',)
        return reply_iters

    def getReplyId(self, post_id):
        return self.getReplyIdAndDepth(post_id)[0]

    def getReplyIdAndDepth(self, post_id):
        reply_id = None
        reply_depth = 0
        nrs = ['1','2','3','4','5','6','7','8','9','0']
        i = len(post_id)
        while i > 0:
            i -= 1
            if post_id[i] in nrs:
                while post_id[i] in nrs or post_id[i] == '-':
                    if post_id[i] == '-':
                        reply_depth += 1
                    i -= 1
                reply_id = post_id[i+1:]
            else:
                break
        if reply_id:
             reply_id = '1' + reply_id
        else:
            reply_id = '1'
        return reply_id, reply_depth

    def getResults(self):
        """ Main function to return list of posts to view, depending on user's selection via URL-para."""
        posts = None
        context = aq_inner(self.context)
        threaded = self.getUrlParaVal('threaded')
        if threaded in bool_true_symbolic_strings:
            if context.Type() == post_portal_type:
                posts = self.getThread(context.getId(), threaded)
            else:
                posts = self.getPosts()
        else:
            if context.Type() == post_portal_type:
                posts = self.getThread(context.getId(), threaded)
            else:
                posts = self.getThreads()
        return posts

    def getThreads(self):
        posts = self.getPosts()
        posts_ids = ()
        for post in posts:
            posts_ids += (post['id'],)

        new_ids = ()
        new_posts = ()

        threads_ids = self.getThreadsIds(posts_ids)

        for thread_id in threads_ids:
            thread_ids = self.getThreadIds(posts_ids, thread_id)
            thread_ids = sorted(thread_ids)
            for thread_id in thread_ids:
                new_ids += (thread_id,)

        for new_id in new_ids:
            for post in posts:
                if post['id'] == new_id:
                    new_posts += (post,)
        
        return new_posts

    def getThread(self, post_id, threaded):
        thread_posts = ()
        posts = self.getPosts()
        thread_id = self.getThreadId(post_id)
        for post in posts:
            post_id = post['id']
            if post_id == thread_id or self.isReply(post_id, thread_id):
                thread_posts += (post,)
        if threaded in bool_true_symbolic_strings:
            thread_posts = sorted(thread_posts, key = lambda post: (post.id))
        return thread_posts

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

    def getThreadIds(self, posts_ids, thread_id):
        thread_ids = ()
        for post_id in posts_ids:
            if post_id == thread_id or self.isReply(post_id, thread_id):
                thread_ids += (post_id,)
        return thread_ids

    def getThreadsIds(self, posts_ids):
        threads_ids = ()
        for post_id in posts_ids:
            if self.getThreadId(post_id) not in threads_ids:
                threads_ids += (self.getThreadId(post_id),)
        return threads_ids

    def getUrlParaVal(self, para):
        val = None
        forum_form = self.request.form
        if para in forum_form:
            val = forum_form[para]
        return val

    def getUrlParaVals(self, para):
        pass

    def isIniPost(self, post_id):
        reply_depth = self.getReplyDepth(post_id)
        if reply_depth == 0: return True
        else: return False

    def isReply(self, post_id, thread_id):
        IS_REPLY = False
        nrs = ['1','2','3','4','5','6','7','8','9','0']
        if len(post_id) >= len(thread_id) + 1 \
        and post_id.startswith(thread_id + '-')\
        and post_id[len(thread_id) + 1] in nrs:
            IS_REPLY =  True
        return IS_REPLY

    def isThreaded(self):
        val = self.getUrlParaVal('threaded')
        if val in bool_true_symbolic_strings: return True
        else: return False

    def render(self):
        return self.index()

    def renderForumHead(self):
        return self.forum_head()

    def renderForumBody(self):
        return self.forum_body()

    def removeParaPair(self, query, para_pair):
        query_splits = query.split(para_pair)
        query_start = query_splits[0][:-1]
        query_end_splits = query_splits[1]
        if type(query_end_splits) == list:
            query_end = '&'.join(query_end_splits)
        else:
            query_end = query_end_splits
        query = query_start + query_end
        if query.startswith('&'):
            query = query[1:]
        return query

    def updateUrlQuery(self, para_pair):
        new_url = None
        url = self.context.absolute_url()
        query = self.request['QUERY_STRING']
        para = para_pair.split('=')[0]
        val = para_pair.split('=')[1]

        if query != '':
            if query.find(para + '=') != -1:
                if para.endswith('%3Alist'):
                    if query.find(para_pair) != -1:
                        query = self.removeParaPair(query, para_pair)
                    else:
                        query += '&' + para_pair
                else:
                    query = self.exchangeParaVal(query, para, val)
            else:
                query += '&' + para_pair
        else:
            query = para_pair
        if query != '': query = '?' + query
        new_url = url + query
        return new_url

#EOF

