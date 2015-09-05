# -*- coding: utf-8 -*-

from plone import api

from Acquisition import aq_inner, aq_parent

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class View(BrowserView):

    def getPostPortalType(self):
        return 'News Item'

    def getResultsTypes(self):
        return ('posts', 'threads')

    index = ViewPageTemplateFile("forum_main.pt")

    forum_head = ViewPageTemplateFile("forum_head.pt")

    forum_body = ViewPageTemplateFile("forum_body.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def renderForumHead(self):
        return self.forum_head()

    def renderForumBody(self):
        return self.forum_body()

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

    def getResultsType(self, url_para='results_type'):
        para = 'results_type'
        results_type = self.getResultsTypes()[0] # default
        paras = self.getUrlParas()
        if para in paras:
            results_type = self.getUrlParaVal(para)
        return results_type

    def getResults(self):
        """ Main function to return list of posts to view, depending on user's selection via URL-para."""

        posts = None
        context = aq_inner(self.context)
        results_type = self.getResultsType()
        if results_type == 'posts':
            if context.Type() == self.getPostPortalType():
                posts = self.getThread(context.getId(), results_type)
            else:
                posts = self.getPosts()
        elif results_type == 'threads':
            if context.Type() == self.getPostPortalType():
                posts = self.getThread(context.getId(), results_type)
            else:
                posts = self.getThreads()
        return posts

    def getPosts(self):
        context = aq_inner(self.context)
        if context.Type() == self.getPostPortalType():
            context = aq_parent(self.context)
        posts = api.content.find(context=context, portal_type=self.getPostPortalType(), sort_on='created', sort_order='reverse')
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

    def getThread(self, post_id, results_type):
        thread_posts = ()
        posts = self.getPosts()
        thread_id = self.getThreadId(post_id)
        for post in posts:
            post_id = post['id']
            if post_id == thread_id or self.isReply(post_id, thread_id):
                thread_posts += (post,)
        if results_type == 'threads':
            thread_posts = sorted(thread_posts, key = lambda post: (post.id))
        return thread_posts

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

#EOF
