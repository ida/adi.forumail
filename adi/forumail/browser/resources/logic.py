# -*- coding: utf-8 -*-

from plone import api

from Acquisition import aq_inner, aq_parent

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class View(BrowserView):

    post_type = 'News Item'

    index = ViewPageTemplateFile("forum.pt")

    forum_head = ViewPageTemplateFile("forum_head.pt")

    posts_template = ViewPageTemplateFile("posts.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def renderForumHead(self):
        return self.forum_head()

    def renderPosts(self):
        return self.posts_template()

    def getForumUrl(self):
        forum_url = None
        context = aq_inner(self.context)
        if context.Type() == self.post_type:
            context = aq_parent(context)
        forum_url = context.absolute_url()
        return forum_url

    def getForumPath(self):
        forum_path = None
        forum_url = self.getForumUrl()
        if forum_url:
            splitted_forum_url = forum_url.split('/');
            forum_path = splitted_forum_url[-2] + '/' + splitted_forum_url[-1];
        return forum_path

    def getAddUrl(self):
        add_url = None
        forum_url = self.getForumUrl()
        if forum_url:
            add_url = forum_url + '/createObject?type_name=' + self.post_type
        return add_url

    def getSearchUrl(self):
        search_url = None
        forum_url = self.getForumUrl()
        if forum_url:
            search_url = forum_url + ''
        return search_url

    def getUrlParas(self):
         pass

    def getPosts(self, sort_order='reverse', sort_on='created'):
        """
        Expects forum-(Folder)- or post-(News Item)-object,
        returns post-objects.
        If self is a forum, returns all posts in forum,
        if self is a post, returns all posts of thread.
        """
        portal_type = 'News Item'
        posts = []
        thread_id = None
        context = aq_inner(self.context)
        if context.Type() == 'News Item':
            context = aq_parent(context)
        posts = api.content.find(context=context, portal_type=portal_type, sort_on=sort_on, sort_order=sort_order)
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

    def getThreads(self):
        """
        Sorted by newest ini-post.
        """
        threads = []
        thread = None
        threads_ids = self.getThreadsIds()
        posts = self.getPosts()

        for thread_id in threads_ids:
            
            i = -1
            while i < len(posts)-1:
                i += 1
            
                post = posts[i]
                post_id = post['id']
                
                if post_id == thread_id:
                    threads.append(posts.pop(i))
            
                    i = -1
                    while i < len(posts)-1:
                        i += 1
            
                        post = posts[i]
                        post_id = post['id']
            
                        if post_id.startswith(thread_id):
                            threads.append(posts.pop(i))
        return threads

